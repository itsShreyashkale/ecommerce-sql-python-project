import pandas as pd
import sqlite3

conn = sqlite3.connect("ecommerce.db")

tables = {
    "customers": "data/customers.csv",
    "sellers": "data/sellers.csv",
    "orders": "data/orders.csv",
    "order_items": "data/order_items.csv",
    "payments": "data/payments.csv",
    "products": "data/products.csv",
    "geolocation": "data/geolocation.csv",
}

for table, path in tables.items():
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df.to_sql(table, conn, if_exists="replace", index=False)
    print(f"✅ {table} loaded — {len(df):,} rows")

conn.close()
print("\n✅ ecommerce.db is ready!")