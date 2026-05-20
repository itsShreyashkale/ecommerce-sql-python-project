-- ============================================================
-- E-COMMERCE DATA ANALYSIS - SQL FILE
-- Compatible with: SQLite (VS Code / DB Browser for SQLite)
-- All 15 questions with outputs matching the presentation PDF
-- ============================================================

-- ============================================================
-- SETUP: Create and populate tables from CSV files
-- In VS Code with SQLite extension, run the .import commands
-- via terminal: sqlite3 ecommerce.db < Ecommerce_Analysis.sql
-- OR use DB Browser for SQLite to import CSVs directly.
-- ============================================================

-- DROP tables if they already exist
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS sellers;
DROP TABLE IF EXISTS geolocation;

-- Create tables
CREATE TABLE customers (
    customer_id TEXT,
    customer_unique_id TEXT,
    customer_zip_code_prefix INTEGER,
    customer_city TEXT,
    customer_state TEXT
);

CREATE TABLE orders (
    order_id TEXT,
    customer_id TEXT,
    order_status TEXT,
    order_purchase_timestamp TEXT,
    order_approved_at TEXT,
    order_delivered_carrier_date TEXT,
    order_delivered_customer_date TEXT,
    order_estimated_delivery_date TEXT
);

CREATE TABLE order_items (
    order_id TEXT,
    order_item_id INTEGER,
    product_id TEXT,
    seller_id TEXT,
    shipping_limit_date TEXT,
    price REAL,
    freight_value REAL
);

CREATE TABLE products (
    product_id TEXT,
    product_category_name TEXT,
    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty INTEGER,
    product_weight_g REAL,
    product_length_cm REAL,
    product_height_cm REAL,
    product_width_cm REAL
);

CREATE TABLE payments (
    order_id TEXT,
    payment_sequential INTEGER,
    payment_type TEXT,
    payment_installments INTEGER,
    payment_value REAL
);

CREATE TABLE sellers (
    seller_id TEXT,
    seller_zip_code_prefix INTEGER,
    seller_city TEXT,
    seller_state TEXT
);

CREATE TABLE geolocation (
    geolocation_zip_code_prefix INTEGER,
    geolocation_lat REAL,
    geolocation_lng REAL,
    geolocation_city TEXT,
    geolocation_state TEXT
);

-- ============================================================
-- IMPORT CSV DATA (run these in sqlite3 terminal)
-- .mode csv
-- .import customers.csv customers
-- .import orders.csv orders
-- .import order_items.csv order_items
-- .import products.csv products
-- .import payments.csv payments
-- .import sellers.csv sellers
-- .import geolocation.csv geolocation
-- ============================================================


-- ============================================================
-- Q1. LIST ALL UNIQUE CITIES WHERE CUSTOMERS ARE LOCATED
-- ============================================================
SELECT DISTINCT customer_city
FROM customers;


-- ============================================================
-- Q2. COUNT THE NUMBER OF ORDERS PLACED IN 2017
-- ============================================================
SELECT COUNT(DISTINCT order_id) AS total_orders_2017
FROM orders
WHERE STRFTIME('%Y', order_purchase_timestamp) = '2017';
-- Expected Output: 45101


-- ============================================================
-- Q3. FIND THE TOTAL SALES PER CATEGORY
-- ============================================================
SELECT p.product_category_name,
       ROUND(SUM(oi.price), 2) AS total_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_sales DESC,
         p.product_category_name ASC;
-- Top results: HEALTH BEAUTY 1258681.34, Watches present 1205005.68, bed table bath 1036988.68


-- ============================================================
-- Q4. CALCULATE THE PERCENTAGE OF ORDERS THAT WERE PAID IN INSTALLMENTS
-- ============================================================
SELECT
    ROUND(
        COUNT(DISTINCT CASE WHEN payment_installments > 1 THEN order_id END) * 100.0
        / COUNT(DISTINCT order_id),
        2
    ) AS installment_percentage
FROM payments;
-- Expected Output: 51.46


-- ============================================================
-- Q5. COUNT THE NUMBER OF CUSTOMERS FROM EACH STATE
-- ============================================================
SELECT customer_state,
       COUNT(*) AS total_customers
FROM customers
GROUP BY customer_state
ORDER BY total_customers DESC;
-- Top: SP 41745, RJ 12852, MG 11635


-- ============================================================
-- Q6. CALCULATE THE NUMBER OF ORDERS PER MONTH IN 2018
-- ============================================================
SELECT
    STRFTIME('%Y-%m', order_purchase_timestamp) AS month,
    COUNT(*) AS total_orders
FROM orders
WHERE STRFTIME('%Y', order_purchase_timestamp) = '2018'
GROUP BY month
ORDER BY month;
-- 2018-01: 7269, 2018-02: 6728, ...


-- ============================================================
-- Q7. FIND THE AVERAGE NUMBER OF PRODUCTS PER ORDER, GROUPED BY CUSTOMER CITY
-- ============================================================
SELECT
    c.customer_city,
    ROUND(AVG(t.product_count), 2) AS avg_products_per_order
FROM (
    SELECT
        oi.order_id,
        COUNT(*) AS product_count
    FROM order_items oi
    GROUP BY oi.order_id
) t
JOIN orders o ON t.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_city
ORDER BY avg_products_per_order DESC,
         c.customer_city ASC;
-- Top: padre carvalho 7.0, celso ramos 6.5, candido godoi 6.0


-- ============================================================
-- Q8. CALCULATE THE PERCENTAGE OF TOTAL REVENUE CONTRIBUTED BY EACH PRODUCT CATEGORY
-- ============================================================
SELECT
    p.product_category_name,
    ROUND(SUM(oi.price), 6) AS category_revenue,
    ROUND(
        SUM(oi.price) * 100.0 /
        (SELECT SUM(price) FROM order_items),
        2
    ) AS revenue_percentage
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY category_revenue DESC;
-- HEALTH BEAUTY: 1258681.34, 9.26%


-- ============================================================
-- Q9. CORRELATION BETWEEN PRODUCT PRICE AND PURCHASE FREQUENCY
-- ============================================================
SELECT
    (
        COUNT(*) * SUM(avg_price * purchase_count)
        - SUM(avg_price) * SUM(purchase_count)
    )
    /
    SQRT(
        (COUNT(*) * SUM(avg_price * avg_price) - (SUM(avg_price) * SUM(avg_price))) *
        (COUNT(*) * SUM(purchase_count * purchase_count) - (SUM(purchase_count) * SUM(purchase_count)))
    ) AS correlation
FROM (
    SELECT
        product_id,
        COUNT(*) AS purchase_count,
        AVG(price) AS avg_price
    FROM order_items
    GROUP BY product_id
) t;
-- Expected Output: ~ -0.0321398625...


-- ============================================================
-- Q10. TOTAL REVENUE BY SELLER AND RANK
-- ============================================================
SELECT
    oi.seller_id,
    ROUND(SUM(oi.price), 6) AS revenue,
    RANK() OVER (ORDER BY SUM(oi.price) DESC) AS rnk
FROM order_items oi
GROUP BY oi.seller_id
ORDER BY revenue DESC;
-- Top seller: 4869f7a5dfa... revenue ~229472.63, rank 1


-- ============================================================
-- Q11. MOVING AVERAGE OF ORDER VALUES FOR EACH CUSTOMER
-- (3-row window: current + 2 preceding)
-- ============================================================
WITH order_value AS (
    SELECT
        c.customer_id,
        o.order_id,
        o.order_purchase_timestamp,
        SUM(oi.price) AS order_value
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.customer_id, o.order_id, o.order_purchase_timestamp
)
SELECT
    customer_id,
    order_id,
    order_purchase_timestamp,
    order_value,
    AVG(order_value) OVER (
        PARTITION BY customer_id
        ORDER BY order_purchase_timestamp
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg
FROM order_value
ORDER BY customer_id, order_purchase_timestamp;


-- ============================================================
-- Q12. CUMULATIVE SALES PER MONTH FOR EACH YEAR
-- ============================================================
SELECT
    year,
    month,
    month_name,
    ROUND(monthly_sales, 6) AS monthly_sales,
    ROUND(cumulative_sales, 6) AS cumulative_sales
FROM (
    SELECT
        STRFTIME('%Y', o.order_purchase_timestamp) AS year,
        STRFTIME('%m', o.order_purchase_timestamp) AS month,
        CASE STRFTIME('%m', o.order_purchase_timestamp)
            WHEN '01' THEN 'January'
            WHEN '02' THEN 'February'
            WHEN '03' THEN 'March'
            WHEN '04' THEN 'April'
            WHEN '05' THEN 'May'
            WHEN '06' THEN 'June'
            WHEN '07' THEN 'July'
            WHEN '08' THEN 'August'
            WHEN '09' THEN 'September'
            WHEN '10' THEN 'October'
            WHEN '11' THEN 'November'
            WHEN '12' THEN 'December'
        END AS month_name,
        SUM(oi.price) AS monthly_sales,
        SUM(SUM(oi.price)) OVER (
            PARTITION BY STRFTIME('%Y', o.order_purchase_timestamp)
            ORDER BY STRFTIME('%m', o.order_purchase_timestamp)
        ) AS cumulative_sales
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY year, month, month_name
) t
ORDER BY year, month;
-- 2016-09: 267.36 | 267.36, 2016-10: 49507.66 | 49775.02 ...


-- ============================================================
-- Q13. YEAR OVER YEAR GROWTH RATE OF TOTAL SALES
-- ============================================================
SELECT
    year,
    ROUND(total_sales, 6) AS total_sales,
    ROUND(LAG(total_sales) OVER (ORDER BY year), 6) AS previous_year_sales,
    ROUND(
        (total_sales - LAG(total_sales) OVER (ORDER BY year))
        / LAG(total_sales) OVER (ORDER BY year) * 100,
        2
    ) AS yoy_growth_percentage
FROM (
    SELECT
        STRFTIME('%Y', o.order_purchase_timestamp) AS year,
        SUM(oi.price) AS total_sales
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY year
) t
ORDER BY year;
-- 2016: 49785.92 | NULL | NULL
-- 2017: 6155806.98 | 49785.92 | 12264.55
-- 2018: 7386050.80 | 6155806.98 | 19.99


-- ============================================================
-- Q14. CUSTOMER RETENTION RATE (within 6 months of first purchase)
-- ============================================================
WITH first_orders AS (
    SELECT
        customer_id,
        MIN(order_purchase_timestamp) AS first_order
    FROM orders
    GROUP BY customer_id
),
repeat_customers AS (
    SELECT DISTINCT o.customer_id
    FROM orders o
    JOIN first_orders f ON o.customer_id = f.customer_id
    WHERE o.order_purchase_timestamp > f.first_order
    AND JULIANDAY(o.order_purchase_timestamp) <= JULIANDAY(f.first_order) + 180
)
SELECT
    ROUND(
        COUNT(DISTINCT r.customer_id) * 100.0 /
        COUNT(DISTINCT f.customer_id),
        2
    ) AS retention_rate
FROM first_orders f
LEFT JOIN repeat_customers r ON f.customer_id = r.customer_id;
-- Expected Output: 0.00


-- ============================================================
-- Q15. TOP 3 CUSTOMERS WHO SPENT THE MOST MONEY IN EACH YEAR
-- ============================================================
SELECT *
FROM (
    SELECT
        STRFTIME('%Y', o.order_purchase_timestamp) AS year,
        o.customer_id,
        SUM(oi.price) AS total_spent,
        RANK() OVER (
            PARTITION BY STRFTIME('%Y', o.order_purchase_timestamp)
            ORDER BY SUM(oi.price) DESC
        ) AS rnk
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY year, o.customer_id
) t
WHERE rnk <= 3
ORDER BY year, rnk;
-- 2016 rank1: a9dc96b... 1399.00
-- 2017 rank1: 1617b13... 13440.00
-- 2018 rank1: ec5b2ba... 7160.00
