import sqlite3
import pandas as pd

conn = sqlite3.connect("ecommerce.db")

# ── Q1: Moving average ─────────────────────────
print("=" * 55)
print("Q1: Moving Average of Order Values per Customer")
print("=" * 55)
df1 = pd.read_sql_query("""
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
    LIMIT 20
""", conn)
print(df1.to_string(index=False))

# ── Q2: Cumulative sales per month ─────────────
print("\n" + "=" * 55)
print("Q2: Cumulative Sales per Month for Each Year")
print("=" * 55)
df2 = pd.read_sql_query("""
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
    ORDER BY year, month
""", conn)
print(df2.to_string(index=False))

# ── Q3: Year over year growth ──────────────────
print("\n" + "=" * 55)
print("Q3: Year-over-Year Growth Rate of Total Sales")
print("=" * 55)
df3 = pd.read_sql_query("""
    SELECT year, total_sales,
        LAG(total_sales) OVER (ORDER BY year) AS prev_year_sales,
        ROUND(100.0 * (total_sales - LAG(total_sales) OVER (ORDER BY year)) 
              / LAG(total_sales) OVER (ORDER BY year), 2) AS yoy_growth_rate
    FROM (
        SELECT strftime('%Y', o.order_purchase_timestamp) AS year,
               ROUND(SUM(oi.price), 2) AS total_sales
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_purchase_timestamp IS NOT NULL
        GROUP BY year
    )
    ORDER BY year
""", conn)
print(df3.to_string(index=False))

# ── Q4: Retention rate ─────────────────────────
print("\n" + "=" * 55)
print("Q4: Customer Retention Rate (within 6 months)")
print("=" * 55)
df4 = pd.read_sql_query("""
    SELECT 
        ROUND(100.0 * COUNT(DISTINCT r.customer_id) / 
              COUNT(DISTINCT fp.customer_id), 2) AS retention_rate
    FROM (
        SELECT customer_id, MIN(order_purchase_timestamp) AS first_date
        FROM orders
        WHERE order_purchase_timestamp IS NOT NULL
        GROUP BY customer_id
    ) fp
    LEFT JOIN (
        SELECT DISTINCT o1.customer_id
        FROM orders o1
        JOIN orders o2 ON o1.customer_id = o2.customer_id
        WHERE o1.order_purchase_timestamp > o2.order_purchase_timestamp
        AND julianday(o1.order_purchase_timestamp) - 
            julianday(o2.order_purchase_timestamp) <= 180
    ) r ON fp.customer_id = r.customer_id
""", conn)
print(df4.to_string(index=False))

# ── Q5: Top 3 customers per year ───────────────
print("\n" + "=" * 55)
print("Q5: Top 3 Customers by Spending per Year")
print("=" * 55)
df5 = pd.read_sql_query("""
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
    ORDER BY year, year_rank
""", conn)
print(df5.to_string(index=False))

conn.close()
print("\n✅ All advanced queries done!")