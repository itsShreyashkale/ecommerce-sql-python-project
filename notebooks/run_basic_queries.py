import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("ecommerce.db")

# ── Q1: Unique cities ──────────────────────────
print("=" * 50)
print("Q1: Unique cities where customers are located")
print("=" * 50)
df1 = pd.read_sql_query("""
    SELECT DISTINCT customer_city
    FROM customers
    ORDER BY customer_city
""", conn)
print(f"Total unique cities: {len(df1)}")
print(df1.head(10).to_string(index=False))

# ── Q2: Orders in 2017 ─────────────────────────
print("\n" + "=" * 50)
print("Q2: Number of orders placed in 2017")
print("=" * 50)
df2 = pd.read_sql_query("""
    SELECT COUNT(*) AS total_orders_2017
    FROM orders
    WHERE strftime('%Y', order_purchase_timestamp) = '2017'
""", conn)
print(df2.to_string(index=False))

# ── Q3: Total sales per category ───────────────
print("\n" + "=" * 50)
print("Q3: Total sales per category")
print("=" * 50)
df3 = pd.read_sql_query("""
    SELECT 
        p.product_category,
        ROUND(SUM(oi.price), 2) AS total_sales
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.product_category
    ORDER BY total_sales DESC
""", conn)
print(df3.to_string(index=False))

# ── Q4: Installment percentage ─────────────────
print("\n" + "=" * 50)
print("Q4: Percentage of orders paid in installments")
print("=" * 50)
df4 = pd.read_sql_query("""
    SELECT 
        ROUND(
            100.0 * SUM(CASE WHEN payment_installments > 1 THEN 1 ELSE 0 END) / COUNT(*),
        2) AS installment_percentage
    FROM payments
""", conn)
print(df4.to_string(index=False))

# ── Q5: Customers per state ────────────────────
print("\n" + "=" * 50)
print("Q5: Number of customers from each state")
print("=" * 50)
df5 = pd.read_sql_query("""
    SELECT 
        customer_state,
        COUNT(*) AS customer_count
    FROM customers
    GROUP BY customer_state
    ORDER BY customer_count DESC
""", conn)
print(df5.to_string(index=False))

conn.close()
print("\n✅ All basic queries done!")