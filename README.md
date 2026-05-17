# E-Commerce Analysis — SQL & Python Project

> Navigating the Future of Online Shopping

---

## Project Overview

This project analyzes a Brazilian E-Commerce dataset using SQL and Python.  
It covers Basic, Intermediate, and Advanced query levels with data visualizations to extract meaningful business insights.

---

## Project By

- Name: Shreyash
- Tools: Python, SQLite, Pandas, Matplotlib
- Platform: VSCode, Google Colab, GitHub

---

## Project Structure

```bash
PYTHON_SQL/
│
├── data/
│   ├── customers.csv
│   ├── geolocation.csv
│   ├── order_items.csv
│   ├── orders.csv
│   ├── payments.csv
│   ├── products.csv
│   └── sellers.csv
│
├── notebooks/
│   ├── SQL_EcommerceQueries_Analaysis.ipynb
│   ├── ecommerce_analysis.ipynb
│   ├── basic_viz.py
│   ├── intermediate_viz.py
│   ├── advance_viz.py
│   ├── run_basic_queries.py
│   ├── run_intermediate_queries.py
│   ├── run_advance_queries.py
│   └── setup_db.py
│
├── sql/
│   ├── basic_queries.sql
│   ├── intermediate_queries.sql
│   ├── advance_queries.sql
│   └── ecommerce.db
│
├── visuals/
│   ├── basic_queries.png
│   ├── basic_queries_viz.png
│   ├── basic_viz.png
│   ├── intermediate_queries_viz.png
│   ├── intermediate_viz.png
│   ├── advanced_queries_viz.png
│   ├── advanced_viz.png
│   ├── Figure_1.png
│   ├── Figure_2.png
│   └── Figure_3.png
│
├── xlsx/
│   ├── customers.xlsx
│   ├── order_items.xlsx
│   ├── orders.xlsx
│   ├── payments.xlsx
│   ├── products.xlsx
│   └── sellers.xlsx
│
├── README.md
├── sql_python_present.pdf
└── sql_python_present.pptx
```

---

## Dataset Overview

| File | Description | Rows |
|------|-------------|------|
| customers.csv | Customer demographic details | 99,441 |
| sellers.csv | Seller information | 3,095 |
| orders.csv | Order history and details | 99,441 |
| order_items.csv | Order items details | 112,650 |
| payments.csv | Payment details | 103,886 |
| products.csv | Product details | 32,951 |
| geolocation.csv | Geolocation details | 1,000,163 |

---

## Tools & Libraries

| Tool | Purpose |
|------|----------|
| Python 3.x | Core programming language |
| SQLite | Database engine |
| Pandas | Data manipulation |
| Matplotlib | Data visualization |
| Google Colab | Notebook environment |
| VSCode | Code editor |
| GitHub | Version control |

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-sql-python-project.git
cd ecommerce-sql-python-project
```

### 2. Install Dependencies

```bash
pip install pandas matplotlib openpyxl seaborn
```

### 3. Setup Database

```bash
python setup_db.py
```

### 4. Run SQL Query Scripts

```bash
python run_basic_queries.py
python run_intermediate_queries.py
python run_advance_queries.py
```

### 5. Run Visualization Scripts

```bash
python basic_viz.py
python intermediate_viz.py
python advance_viz.py
```

---

## Basic Queries

Objective: Extract fundamental insights from the dataset.

| Query | Result |
|--------|---------|
| Unique cities where customers are located | 4,119 unique cities |
| Number of orders placed in 2017 | 45,101 orders |
| Total sales per category | Health & Beauty — R$1.25M |
| Percentage of orders paid in installments | 49.42% |
| Number of customers from each state | SP leads with 41,746 |

### Visualization

```text
visuals/basic_viz.png
```

---

## Intermediate Queries

Objective: Analyze sales and order trends in greater detail.

| Query | Result |
|--------|---------|
| Orders per month in 2018 | January peak — 6,288 orders |
| Average products per order by city | Padre Carvalho — 7 products/order |
| Revenue percentage by category | Health & Beauty — 9.26% |
| Price vs purchase frequency | Most purchased product — 527 times |
| Total revenue by seller ranked | Top seller — R$229,472 |

### Visualization

```text
visuals/intermediate_viz.png
```

---

## Advanced Queries

Objective: Generate strategic and customer-centric insights.

| Query | Result |
|--------|---------|
| Moving average of order values | Tracks customer spending trends |
| Cumulative sales per month | 2018 reached R$6.35M by August |
| Year-over-year growth rate | 2017 grew 12,745% vs 2016 |
| Customer retention rate | Most customers purchase only once |
| Top 3 customers per year | 2017 top spender — R$13,440 |

### Visualization

```text
visuals/advanced_viz.png
```

---

## Key Business Insights

1. São Paulo dominates the customer base with approximately 42% of customers.
2. Health & Beauty is the highest-performing category with R$1.25M in sales.
3. Nearly half of customers prefer installment payments.
4. Business growth accelerated significantly during 2017.
5. Customer retention is low, indicating opportunities for loyalty programs.
6. Seasonal sales peaks are visible during high-shopping periods such as November.

---

## Google Colab Notebook

All SQL queries and Python visualizations are available in the notebook:

```text
notebooks/ecommerce_analysis.ipynb
```
