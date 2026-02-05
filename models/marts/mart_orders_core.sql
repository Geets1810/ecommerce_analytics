{{ config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='sync_all_columns'
) }}

WITH orders AS (
    SELECT
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp::date AS order_date,
        order_delivered_customer_date,
        order_estimated_delivery_date
    FROM {{ ref('stg_orders') }}

    {% if is_incremental() %}
      WHERE order_purchase_timestamp > (
          SELECT max(order_date) FROM {{ this }}
      )
    {% endif %}
),

customers AS (
    SELECT
        customer_id,
        customer_state
    FROM {{ ref('stg_customers') }}
),

payments AS (
  SELECT
    order_id,
    COALESCE(SUM(payment_value), 0) AS total_order_value,
    MAX(payment_type) AS payment_type
  FROM {{ ref('stg_payments') }}
  GROUP BY order_id
),

delivery_metrics AS (
    SELECT
        order_id,
        DATE_DIFF(
            'day',
            order_purchase_timestamp,
            order_delivered_customer_date
        ) AS delivery_days
    FROM {{ ref('stg_orders') }}
)

SELECT
    o.order_id,
    o.order_date,
    o.order_status,
    o.customer_id,
    c.customer_state,
    COALESCE(p.total_order_value, 0) AS total_order_value,
    CASE WHEN p.order_id IS NULL THEN 1 ELSE 0 END AS is_unpaid_order,
    p.payment_type,
    d.delivery_days
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN payments p ON o.order_id = p.order_id
LEFT JOIN delivery_metrics d ON o.order_id = d.order_id
