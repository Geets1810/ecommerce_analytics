-- Product dimension with sales metrics
select
    p.product_id,
    p.product_category_name,
    count(distinct oi.order_id) as times_ordered,
    sum(oi.price) as total_revenue,
    avg(oi.price) as avg_price
from {{ ref('stg_products') }} p
left join {{ ref('stg_order_items') }} oi
    on p.product_id = oi.product_id
group by 1, 2
