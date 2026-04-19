-- ================================================
--   INTERMEDIATE QUERIES — E-Commerce Analysis
-- ================================================

-- Q1: Calculate the number of orders per month in 2018
SELECT 
    strftime('%m', order_purchase_timestamp) AS month,
    COUNT(*) AS total_orders
FROM orders
WHERE strftime('%Y', order_purchase_timestamp) = '2018'
GROUP BY month
ORDER BY month;

-- Q2: Find the average number of products per order
--     grouped by customer city
-- Q2: Find the average number of products per order
--     grouped by customer city
SELECT 
    c.customer_city,
    ROUND(AVG(oi.item_count), 2) AS avg_products_per_order
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN (
    SELECT order_id, COUNT(*) AS item_count
    FROM order_items
    GROUP BY order_id
) oi ON o.order_id = oi.order_id
GROUP BY c.customer_city
HAVING COUNT(*) > 10
ORDER BY avg_products_per_order DESC
LIMIT 20;

-- Q3: Percentage of total revenue by each product category
SELECT 
    p.product_category,
    ROUND(SUM(oi.price), 2) AS category_revenue,
    ROUND(100.0 * SUM(oi.price) / (SELECT SUM(price) FROM order_items), 2) AS revenue_percentage
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category
ORDER BY revenue_percentage DESC;

-- Q4: Correlation between product price and purchase frequency
SELECT 
    p.product_id,
    ROUND(AVG(oi.price), 2) AS avg_price,
    COUNT(oi.order_id) AS purchase_count
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id
ORDER BY purchase_count DESC
LIMIT 20;

-- Q5: Total revenue by each seller ranked by revenue
SELECT 
    oi.seller_id,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    RANK() OVER (ORDER BY SUM(oi.price) DESC) AS revenue_rank
FROM order_items oi
GROUP BY oi.seller_id
ORDER BY revenue_rank
LIMIT 20;