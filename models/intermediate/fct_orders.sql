select
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp,
    order_delivered_customer_date,
    date_part('year', order_purchase_timestamp) as order_year,
    date_part('month', order_purchase_timestamp) as order_month
from {{ ref('stg_orders') }}
