-- Orders with customer, payment, and review details
select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    c.customer_city,
    c.customer_state,
    sum(p.payment_value) as total_payment,
    max(r.review_score) as review_score
from {{ ref('stg_orders') }} o
left join {{ ref('stg_customers') }} c
    on o.customer_id = c.customer_id
left join {{ ref('stg_payments') }} p
    on o.order_id = p.order_id
left join {{ ref('stg_reviews') }} r
    on o.order_id = r.order_id
group by 1, 2, 3, 4, 5, 6, 7, 8
