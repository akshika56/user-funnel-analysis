-- User Funnel Analysis
-- Signup → Product View → Add to Cart → Checkout

WITH funnel AS (
    SELECT
        user_id,
        MAX(CASE WHEN event_name = 'signup' THEN 1 ELSE 0 END) AS signup,
        MAX(CASE WHEN event_name = 'product_view' THEN 1 ELSE 0 END) AS product_view,
        MAX(CASE WHEN event_name = 'add_to_cart' THEN 1 ELSE 0 END) AS add_to_cart,
        MAX(CASE WHEN event_name = 'checkout' THEN 1 ELSE 0 END) AS checkout
    FROM events
    GROUP BY user_id
)

SELECT
    COUNT(DISTINCT user_id) AS total_users,
    SUM(signup) AS signup_users,
    SUM(product_view) AS product_view_users,
    SUM(add_to_cart) AS add_to_cart_users,
    SUM(checkout) AS checkout_users
FROM funnel;
