{{ config(materialized='table') }}

SELECT
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    p.product_category_name,
    o.customer_id,
    c.customer_state,
    c.customer_city,
    o.order_purchase_timestamp::date as order_date,
    date_part('year', o.order_purchase_timestamp) as order_year,
    date_part('month', o.order_purchase_timestamp) as order_month,
    oi.price,
    oi.freight_value,
    oi.item_total
FROM {{ ref('stg_order_items') }} oi
JOIN {{ ref('stg_orders') }} o
    ON oi.order_id = o.order_id
JOIN {{ ref('stg_customers') }} c
    ON o.customer_id = c.customer_id
JOIN {{ ref('stg_products') }} p
    ON oi.product_id = p.product_id
