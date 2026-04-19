-- ================================================
--   BASIC QUERIES — E-Commerce Analysis
-- ================================================

-- Q1: List all unique cities where customers are located
SELECT DISTINCT customer_city
FROM customers
ORDER BY customer_city;

-- Q2: Count the number of orders placed in 2017
SELECT COUNT(*) AS total_orders_2017
FROM orders
WHERE strftime('%Y', order_purchase_timestamp) = '2017';

-- Q3: Find the total sales per category
SELECT 
    p.product_category,
    ROUND(SUM(oi.price), 2) AS total_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category
ORDER BY total_sales DESC;

-- Q4: Calculate the percentage of orders paid in installments
SELECT 
    ROUND(
        100.0 * SUM(CASE WHEN payment_installments > 1 THEN 1 ELSE 0 END) / COUNT(*),
    2) AS installment_percentage
FROM payments;

-- Q5: Count the number of customers from each state
SELECT 
    customer_state,
    COUNT(*) AS customer_count
FROM customers
GROUP BY customer_state
ORDER BY customer_count DESC;