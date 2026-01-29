select
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state,
    count(order_id) as lifetime_orders,
    min(order_purchase_timestamp) as first_order_date,
    max(order_purchase_timestamp) as last_order_date
from {{ ref('int_customer_orders') }}
group by 1, 2, 3, 4
