import sqlite3
import pandas as pd

conn = sqlite3.connect("ecommerce.db")

# ── Q1: Orders per month in 2018 ───────────────
print("=" * 55)
print("Q1: Number of orders per month in 2018")
print("=" * 55)
df1 = pd.read_sql_query("""
    SELECT strftime('%m', order_purchase_timestamp) AS month,
           COUNT(*) AS total_orders
    FROM orders
    WHERE strftime('%Y', order_purchase_timestamp) = '2018'
    AND order_purchase_timestamp IS NOT NULL
    GROUP BY month ORDER BY month
""", conn)
print(df1.to_string(index=False))

# ── Q2: Avg products per order by city ─────────
print("\n" + "=" * 55)
print("Q2: Avg products per order by customer city (Top 20)")
print("=" * 55)
df2 = pd.read_sql_query("""
    SELECT c.customer_city,
           ROUND(AVG(item_count), 2) AS avg_products_per_order
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN (
        SELECT order_id, COUNT(*) AS item_count
        FROM order_items GROUP BY order_id
    ) oi ON o.order_id = oi.order_id
    GROUP BY c.customer_city
    ORDER BY avg_products_per_order DESC
    LIMIT 20
""", conn)
print(df2.to_string(index=False))

# ── Q3: Revenue percentage by category ─────────
print("\n" + "=" * 55)
print("Q3: Revenue percentage by product category")
print("=" * 55)
df3 = pd.read_sql_query("""
    SELECT p.product_category,
           ROUND(SUM(oi.price), 2) AS category_revenue,
           ROUND(100.0 * SUM(oi.price) / 
                (SELECT SUM(price) FROM order_items), 2) AS revenue_percentage
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.product_category
    ORDER BY revenue_percentage DESC
""", conn)
print(df3.to_string(index=False))

# ── Q4: Price vs purchase frequency ────────────
print("\n" + "=" * 55)
print("Q4: Product price vs purchase frequency (Top 20)")
print("=" * 55)
df4 = pd.read_sql_query("""
    SELECT p.product_id,
           ROUND(AVG(oi.price), 2) AS avg_price,
           COUNT(oi.order_id) AS purchase_count
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.product_id
    ORDER BY purchase_count DESC
    LIMIT 20
""", conn)
print(df4.to_string(index=False))

# ── Q5: Seller revenue ranking ─────────────────
print("\n" + "=" * 55)
print("Q5: Total revenue by seller — Top 20")
print("=" * 55)
df5 = pd.read_sql_query("""
    SELECT oi.seller_id,
           ROUND(SUM(oi.price), 2) AS total_revenue,
           RANK() OVER (ORDER BY SUM(oi.price) DESC) AS revenue_rank
    FROM order_items oi
    GROUP BY oi.seller_id
    ORDER BY revenue_rank
    LIMIT 20
""", conn)
print(df5.to_string(index=False))

conn.close()
print("\n✅ All intermediate queries done!")