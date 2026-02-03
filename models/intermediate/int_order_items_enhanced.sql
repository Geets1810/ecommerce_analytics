-- Order items with product and seller details
select
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    oi.price,
    oi.freight_value,
    oi.item_total,
    p.product_category_name,
    s.seller_city,
    s.seller_state
from {{ ref('stg_order_items') }} oi
left join {{ ref('stg_products') }} p
    on oi.product_id = p.product_id
left join {{ ref('stg_sellers') }} s
    on oi.seller_id = s.seller_id
