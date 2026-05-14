import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("ecommerce.db")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Intermediate Queries — E-Commerce Analysis",
             fontsize=18, fontweight='bold')

# ── Q1: Orders per month in 2018 ───────────────
df1 = pd.read_sql_query("""
    SELECT strftime('%m', order_purchase_timestamp) AS month,
           COUNT(*) AS total_orders
    FROM orders
    WHERE strftime('%Y', order_purchase_timestamp) = '2018'
    AND order_purchase_timestamp IS NOT NULL
    GROUP BY month ORDER BY month
""", conn)
month_names = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct']
df1 = df1[df1['total_orders'] > 10]
axes[0,0].plot(month_names[:len(df1)], df1['total_orders'],
               marker='o', color='#2196F3', linewidth=2.5,
               markersize=8)
axes[0,0].fill_between(month_names[:len(df1)],
                        df1['total_orders'], alpha=0.2,
                        color='#2196F3')
axes[0,0].set_title('Q1: Orders per Month in 2018')
axes[0,0].set_xlabel('Month')
axes[0,0].set_ylabel('Number of Orders')
for i, v in enumerate(df1['total_orders']):
    axes[0,0].text(i, v + 50, f'{v:,}',
                   ha='center', fontsize=8, fontweight='bold')

# ── Q2: Top 10 cities avg products per order ───
df2 = pd.read_sql_query("""
    SELECT c.customer_city,
           ROUND(AVG(oi.item_count), 2) AS avg_products
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN (
        SELECT order_id, COUNT(*) AS item_count
        FROM order_items GROUP BY order_id
    ) oi ON o.order_id = oi.order_id
    GROUP BY c.customer_city
    HAVING COUNT(*) > 10
    ORDER BY avg_products DESC
    LIMIT 10
""", conn)
axes[0,1].barh(df2['customer_city'][::-1],
               df2['avg_products'][::-1],
               color='#4CAF50')
axes[0,1].set_title('Q2: Avg Products per Order by City (Top 10)')
axes[0,1].set_xlabel('Avg Products per Order')

# ── Q3: Top 10 categories by revenue % ─────────
df3 = pd.read_sql_query("""
    SELECT p.product_category,
           ROUND(100.0 * SUM(oi.price) /
                (SELECT SUM(price) FROM order_items), 2) AS revenue_pct
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.product_category
    ORDER BY revenue_pct DESC
    LIMIT 10
""", conn)
axes[1,0].bar(range(len(df3)), df3['revenue_pct'],
              color='#FF9800')
axes[1,0].set_xticks(range(len(df3)))
axes[1,0].set_xticklabels(
    [c[:12] for c in df3['product_category']],
    rotation=45, ha='right', fontsize=8)
axes[1,0].set_title('Q3: Revenue % by Category (Top 10)')
axes[1,0].set_ylabel('Revenue Percentage (%)')
for i, v in enumerate(df3['revenue_pct']):
    axes[1,0].text(i, v + 0.1, f'{v}%',
                   ha='center', fontsize=7, fontweight='bold')

# ── Q5: Top 10 sellers by revenue ──────────────
df5 = pd.read_sql_query("""
    SELECT oi.seller_id,
           ROUND(SUM(oi.price), 2) AS total_revenue
    FROM order_items oi
    GROUP BY oi.seller_id
    ORDER BY total_revenue DESC
    LIMIT 10
""", conn)
df5['seller_short'] = df5['seller_id'].str[:8] + '...'
axes[1,1].bar(df5['seller_short'], df5['total_revenue'],
              color='#9C27B0')
axes[1,1].set_title('Q5: Top 10 Sellers by Revenue')
axes[1,1].set_xlabel('Seller ID')
axes[1,1].set_ylabel('Total Revenue (R$)')
axes[1,1].tick_params(axis='x', rotation=45)
for i, v in enumerate(df5['total_revenue']):
    axes[1,1].text(i, v + 1000, f'R${v/1000:.0f}K',
                   ha='center', fontsize=7, fontweight='bold')

plt.tight_layout()
plt.savefig('visuals/intermediate_queries_viz.png',
            dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart saved in visuals folder!")

conn.close()