-- Order fact table with all metrics
select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    date_part('year', o.order_purchase_timestamp) as order_year,
    date_part('month', o.order_purchase_timestamp) as order_month,
    date_part('quarter', o.order_purchase_timestamp) as order_quarter,
    o.customer_city,
    o.customer_state,
    o.total_payment as order_total,
    o.review_score,
    count(oi.order_item_id) as items_in_order,
    sum(oi.price) as product_value,
    sum(oi.freight_value) as freight_value
from {{ ref('int_orders_enhanced') }} o
left join {{ ref('int_order_items_enhanced') }} oi
    on o.order_id = oi.order_id
group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
