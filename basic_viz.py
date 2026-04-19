import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("ecommerce.db")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Basic Queries — E-Commerce Analysis", 
             fontsize=18, fontweight='bold')

# ── Q2: Orders per Year ────────────────────────
df2 = pd.read_sql_query("""
    SELECT strftime('%Y', order_purchase_timestamp) AS year, 
           COUNT(*) AS total_orders
    FROM orders
    WHERE order_purchase_timestamp IS NOT NULL
    GROUP BY year ORDER BY year
""", conn)
df2 = df2.dropna(subset=['year'])
df2['year'] = df2['year'].astype(str)
axes[0,0].bar(df2['year'], df2['total_orders'], 
              color=['#2196F3','#E91E63','#4CAF50'])
axes[0,0].set_title('Q2: Orders per Year')
axes[0,0].set_xlabel('Year')
axes[0,0].set_ylabel('Number of Orders')
for i, v in enumerate(df2['total_orders']):
    axes[0,0].text(i, v + 200, f'{v:,}', ha='center', fontweight='bold')

# ── Q3: Top 10 Categories by Sales ────────────
df3 = pd.read_sql_query("""
    SELECT p.product_category,
           ROUND(SUM(oi.price), 2) AS total_sales
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.product_category
    ORDER BY total_sales DESC LIMIT 10
""", conn)
axes[0,1].barh(df3['product_category'][::-1], 
               df3['total_sales'][::-1], color='#FF9800')
axes[0,1].set_title('Q3: Top 10 Categories by Sales')
axes[0,1].set_xlabel('Total Sales (R$)')

# ── Q4: Installments Pie Chart ─────────────────
sizes = [49.42, 50.58]
labels = ['Installments\n49.42%', 'Full Payment\n50.58%']
axes[1,0].pie(sizes, labels=labels, 
              colors=['#E91E63','#2196F3'],
              autopct='%1.1f%%', startangle=90)
axes[1,0].set_title('Q4: Payment Method Breakdown')

# ── Q5: Top 10 States by Customers ────────────
df5 = pd.read_sql_query("""
    SELECT customer_state, COUNT(*) AS customer_count
    FROM customers
    GROUP BY customer_state
    ORDER BY customer_count DESC LIMIT 10
""", conn)
axes[1,1].bar(df5['customer_state'], df5['customer_count'], 
              color='#9C27B0')
axes[1,1].set_title('Q5: Top 10 States by Customers')
axes[1,1].set_xlabel('State')
axes[1,1].set_ylabel('Number of Customers')

plt.tight_layout()
plt.savefig('visuals/basic_queries_viz.png', 
            dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart saved in visuals folder!")

conn.close()