{{ config(
    materialized='incremental',
    unique_key='product_perf_key',
    on_schema_change='sync_all_columns'
) }}

WITH order_items AS (
    SELECT
        oi.order_id,
        oi.product_id,
        oi.price,
        o.order_purchase_timestamp::date AS order_date,
        c.customer_state
    FROM {{ ref('stg_order_items') }} oi
    JOIN {{ ref('stg_orders') }} o
      ON oi.order_id = o.order_id
    JOIN {{ ref('stg_customers') }} c
      ON o.customer_id = c.customer_id

    {% if is_incremental() %}
      WHERE o.order_purchase_timestamp > (
          SELECT max(order_date) FROM {{ this }}
      )
    {% endif %}
),

products AS (
    SELECT
        product_id,
        product_category_name
    FROM {{ ref('stg_products') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key([
        'oi.product_id',
        'oi.order_date',
        'oi.customer_state'
    ]) }} AS product_perf_key,

    oi.product_id,
    p.product_category_name,
    oi.order_date,
    oi.customer_state,

    COUNT(DISTINCT oi.order_id) AS orders_count,
    SUM(oi.price) AS revenue,
    AVG(oi.price) AS avg_price

FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY
    oi.product_id,
    p.product_category_name,
    oi.order_date,
    oi.customer_state
