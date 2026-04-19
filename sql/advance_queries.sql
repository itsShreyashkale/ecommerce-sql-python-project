-- ================================================
--   ADVANCED QUERIES — E-Commerce Analysis
-- ================================================

-- Q1: Moving average of order values for each customer
SELECT 
    o.customer_id,
    o.order_id,
    o.order_purchase_timestamp,
    ROUND(SUM(oi.price), 2) AS order_value,
    ROUND(AVG(SUM(oi.price)) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_purchase_timestamp
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.customer_id, o.order_purchase_timestamp
ORDER BY o.customer_id, o.order_purchase_timestamp
LIMIT 20;

-- Q2: Cumulative sales per month for each year
SELECT 
    strftime('%Y', o.order_purchase_timestamp) AS year,
    strftime('%m', o.order_purchase_timestamp) AS month,
    ROUND(SUM(oi.price), 2) AS monthly_sales,
    ROUND(SUM(SUM(oi.price)) OVER (
        PARTITION BY strftime('%Y', o.order_purchase_timestamp)
        ORDER BY strftime('%m', o.order_purchase_timestamp)
    ), 2) AS cumulative_sales
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_purchase_timestamp IS NOT NULL
GROUP BY year, month
ORDER BY year, month;

-- Q3: Year-over-year growth rate of total sales
SELECT 
    year,
    total_sales,
    LAG(total_sales) OVER (ORDER BY year) AS prev_year_sales,
    ROUND(100.0 * (total_sales - LAG(total_sales) OVER (ORDER BY year)) 
          / LAG(total_sales) OVER (ORDER BY year), 2) AS yoy_growth_rate
FROM (
    SELECT 
        strftime('%Y', o.order_purchase_timestamp) AS year,
        ROUND(SUM(oi.price), 2) AS total_sales
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_purchase_timestamp IS NOT NULL
    GROUP BY year
) yearly_sales
ORDER BY year;

-- Q4: Retention rate — customers who purchase again within 6 months
SELECT 
    ROUND(100.0 * COUNT(DISTINCT returning.customer_id) / 
          COUNT(DISTINCT first_purchase.customer_id), 2) AS retention_rate
FROM (
    SELECT customer_id, MIN(order_purchase_timestamp) AS first_date
    FROM orders
    WHERE order_purchase_timestamp IS NOT NULL
    GROUP BY customer_id
) first_purchase
LEFT JOIN (
    SELECT DISTINCT o1.customer_id
    FROM orders o1
    JOIN orders o2 ON o1.customer_id = o2.customer_id
    WHERE o1.order_purchase_timestamp > o2.order_purchase_timestamp
    AND julianday(o1.order_purchase_timestamp) - 
        julianday(o2.order_purchase_timestamp) <= 180
) returning ON first_purchase.customer_id = returning.customer_id;

-- Q5: Top 3 customers who spent most money each year
SELECT year, customer_id, total_spent, year_rank
FROM (
    SELECT 
        strftime('%Y', o.order_purchase_timestamp) AS year,
        o.customer_id,
        ROUND(SUM(oi.price), 2) AS total_spent,
        RANK() OVER (
            PARTITION BY strftime('%Y', o.order_purchase_timestamp)
            ORDER BY SUM(oi.price) DESC
        ) AS year_rank
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_purchase_timestamp IS NOT NULL
    GROUP BY year, o.customer_id
)
WHERE year_rank <= 3
ORDER BY year, year_rank;