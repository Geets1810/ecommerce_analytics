-- Customer dimension with lifetime metrics
select
    c.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    count(o.order_id) as lifetime_orders,
    sum(o.order_total) as lifetime_value,
    min(o.order_purchase_timestamp) as first_order_date,
    max(o.order_purchase_timestamp) as last_order_date,
    avg(o.review_score) as avg_review_score
from {{ ref('stg_customers') }} c
left join {{ ref('fct_orders') }} o
    on c.customer_id = o.customer_id
group by 1, 2, 3, 4
