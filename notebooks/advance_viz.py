import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("ecommerce.db")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Advanced Queries — E-Commerce Analysis",
             fontsize=18, fontweight='bold')

# ── Q2: Cumulative sales per year ──────────────
df2 = pd.read_sql_query("""
    SELECT 
        strftime('%Y', o.order_purchase_timestamp) AS year,
        strftime('%m', o.order_purchase_timestamp) AS month,
        ROUND(SUM(SUM(oi.price)) OVER (
            PARTITION BY strftime('%Y', o.order_purchase_timestamp)
            ORDER BY strftime('%m', o.order_purchase_timestamp)
        ), 2) AS cumulative_sales
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_purchase_timestamp IS NOT NULL
    AND strftime('%Y', o.order_purchase_timestamp) IN ('2017','2018')
    GROUP BY year, month
    ORDER BY year, month
""", conn)
for yr, grp in df2.groupby('year'):
    axes[0,0].plot(grp['month'], grp['cumulative_sales']/1000,
                   marker='o', label=yr, linewidth=2.5)
axes[0,0].set_title('Q2: Cumulative Sales per Month by Year')
axes[0,0].set_xlabel('Month')
axes[0,0].set_ylabel('Cumulative Sales (R$ Thousands)')
axes[0,0].legend()

# ── Q3: Year over year growth ──────────────────
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
        AND strftime('%Y', o.order_purchase_timestamp) IN ('2016','2017','2018')
        GROUP BY year
    )
    ORDER BY year
""", conn)
bars = axes[0,1].bar(df3['year'], df3['total_sales']/1000,
                     color=['#2196F3','#4CAF50','#FF9800'])
axes[0,1].set_title('Q3: Total Sales by Year (with YoY Growth)')
axes[0,1].set_xlabel('Year')
axes[0,1].set_ylabel('Total Sales (R$ Thousands)')
for i, (v, g) in enumerate(zip(df3['total_sales'],
                                df3['yoy_growth_rate'])):
    label = f'R${v/1000:.0f}K' if pd.isna(g) else f'R${v/1000:.0f}K\n({g}%)'
    axes[0,1].text(i, v/1000 + 50, label,
                   ha='center', fontsize=8, fontweight='bold')

# ── Q5: Top spenders per year ──────────────────
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
        AND strftime('%Y', o.order_purchase_timestamp) IN ('2016','2017','2018')
        GROUP BY year, o.customer_id
    )
    WHERE year_rank <= 3
    ORDER BY year, year_rank
""", conn)
colors = ['#FFD700','#C0C0C0','#CD7F32']
for i, yr in enumerate(['2016','2017','2018']):
    grp = df5[df5['year'] == yr].reset_index(drop=True)
    x = [i*4 + j for j in range(len(grp))]
    for j, row in grp.iterrows():
        color_idx = min(j, len(colors)-1)
        axes[1,0].bar(i*4+j, row['total_spent'],
                  color=colors[color_idx], edgecolor='white')
        axes[1,0].text(i*4+j, row['total_spent'] + 50,
                   f"R${row['total_spent']:,.0f}",
                   ha='center', fontsize=7, fontweight='bold')
axes[1,0].set_title('Q5: Top 3 Customers by Spending per Year')
axes[1,0].set_ylabel('Total Spent (R$)')
axes[1,0].set_xticks([1, 5, 9])
axes[1,0].set_xticklabels(['2016', '2017', '2018'])
gold = plt.Rectangle((0,0),1,1, color='#FFD700', label='Rank 1')
silver = plt.Rectangle((0,0),1,1, color='#C0C0C0', label='Rank 2')
bronze = plt.Rectangle((0,0),1,1, color='#CD7F32', label='Rank 3')
axes[1,0].legend(handles=[gold, silver, bronze])

# ── Q4: Retention rate visual ──────────────────
labels = ['Retained\nCustomers\n(0%)', 'One-time\nCustomers\n(100%)']
sizes = [0.1, 99.9]
axes[1,1].pie(sizes, labels=labels,
              colors=['#4CAF50','#FF5722'],
              autopct='%1.1f%%', startangle=90)
axes[1,1].set_title('Q4: Customer Retention Rate\n(within 6 months)')

plt.tight_layout()
plt.savefig('visuals/advanced_queries_viz.png',
            dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart saved in visuals folder!")

conn.close()