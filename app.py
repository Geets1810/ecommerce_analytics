import streamlit as st
import duckdb
import anthropic
import os
import pandas as pd
from datetime import datetime
from io import BytesIO

# Page config
st.set_page_config(
    page_title="Self-Service Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# Initialize Claude API
@st.cache_resource
def get_claude_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY environment variable not set")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)

client = get_claude_client()

# Database connection
@st.cache_resource
def get_db_connection():
    return duckdb.connect('ecommerce_analytics.duckdb', read_only=True)

conn = get_db_connection()

# Get schema info
@st.cache_data
def get_schema_info():
    schema_query = """
    SELECT
        table_name,
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema = 'main'
    AND table_name IN ('fct_orders', 'fct_order_items', 'dim_customers', 'dim_products')
    ORDER BY table_name, ordinal_position
    """
    return conn.execute(schema_query).fetchdf()

schema_df = get_schema_info()

# Title
st.title("🤖 Self-Service Analytics Platform")
st.markdown("*Ask questions in plain English, get instant SQL-powered answers*")

# Sidebar - Available Data
with st.sidebar:
    st.header("📊 Available Data")

    st.subheader("Tables:")
    st.markdown("""
    - **fct_orders**: Order transactions with revenue
    - **dim_customers**: Customer information & lifetime metrics
    - **dim_products**: Product catalog & sales metrics
    """)

    with st.expander("View Schema Details"):
        st.dataframe(schema_df, use_container_width=True)

    st.markdown("---")
    st.markdown("**Example Questions:**")
    st.markdown("""
    - What was total revenue last month?
    - Who are the top 10 customers by lifetime value?
    - Which state has the most orders?
    - Show me monthly revenue trend for 2024
    - What's the average order value?
    """)

# Main interface
st.subheader("💬 Ask Your Question")

# Sample question buttons
st.markdown("**Try these examples:**")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Total Revenue 2017", use_container_width=True):
        st.session_state.question_input = "What was total revenue in 2017?"
    if st.button("🏆 Top 10 Customers", use_container_width=True):
        st.session_state.question_input = "Who are the top 10 customers by lifetime value?"

with col2:
    if st.button("📍 Orders by State", use_container_width=True):
        st.session_state.question_input = "Which state has the most orders?"
    if st.button("📈 Monthly Revenue Trend", use_container_width=True):
        st.session_state.question_input = "Show me monthly revenue trend for 2017"

with col3:
    if st.button("💰 Average Order Value", use_container_width=True):
        st.session_state.question_input = "What is the average order value?"
    if st.button("⭐ Top Products", use_container_width=True):
        st.session_state.question_input = "What are the top 10 products by revenue?"

st.markdown("---")

# Text input (now with session state)
user_question = st.text_input(
    "Or type your own question:",
    value=st.session_state.get("question_input", ""),
    placeholder="e.g., What was total revenue in January 2024?",
    key="question_input"
)

if user_question:
    with st.spinner("🤔 Translating to SQL..."):
        # Build prompt for Claude
        prompt = f"""You are a SQL expert analyzing an e-commerce database.

            **CRITICAL: You can ONLY use these tables:**
            - fct_orders (order-level metrics: one row per order)
            - fct_order_items (product-level metrics: one row per item sold - USE THIS for product questions)
            - dim_customers (customer attributes)
            - dim_products (product attributes)

            **Available columns:**
            {schema_df.to_string()}

            **Join rules:**
            - fct_orders.customer_id → dim_customers.customer_id
            - fct_order_items.product_id → dim_products.product_id
            - fct_order_items.customer_state (already has state, no join needed)

            **Important:**
            - For PRODUCT questions, use fct_order_items (not fct_orders)
            - Use DuckDB SQL syntax
            - Do NOT use tables not listed above
            - Do NOT join order_id to product_id

            User question: {user_question}

            Generate ONLY the SQL query. No explanation.
            """

        try:
            # Call Claude API
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            sql_query = message.content[0].text

            # Clean SQL (remove markdown if present)
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

            # Display generated SQL
            st.code(sql_query, language="sql")

            # Execute query
            with st.spinner("⚡ Running query..."):
                results = conn.execute(sql_query).fetchdf()

            if len(results) == 0:
                st.warning("No results found for this query.")
            else:
                st.success(f"✅ Found {len(results)} rows")

                # Display results
                st.dataframe(results, use_container_width=True)

                # Simple visualization if applicable
                if len(results.columns) == 2 and results[results.columns[1]].dtype in ['float64', 'int64']:
                    st.bar_chart(results.set_index(results.columns[0]))

                # Export options
                st.markdown("### 📥 Export Results")

                col1, col2 = st.columns(2)

                with col1:
                    # Excel export
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        # Summary sheet
                        summary_df = pd.DataFrame({
                            'Report Generated': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                            'Question': [user_question],
                            'Rows Returned': [len(results)]
                        })
                        summary_df.to_excel(writer, sheet_name='Summary', index=False)

                        # Results sheet
                        results.to_excel(writer, sheet_name='Results', index=False)

                    output.seek(0)

                    st.download_button(
                        label="📊 Download Excel",
                        data=output,
                        file_name=f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

                with col2:
                    # CSV export
                    csv = results.to_csv(index=False)
                    st.download_button(
                        label="📄 Download CSV",
                        data=csv,
                        file_name=f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Try rephrasing your question or check the available tables in the sidebar.")

# Footer
st.markdown("---")
st.markdown("*Powered by dbt + DuckDB + Claude API*")
