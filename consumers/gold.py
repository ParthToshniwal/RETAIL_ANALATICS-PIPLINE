import pandas as pd
import os

SILVER_FILE = "landing/silver/transactions.parquet"
GOLD_DIR = "landing/gold"

os.makedirs(GOLD_DIR, exist_ok=True)

print("=" * 60)
print("GOLD ANALYTICS STARTED")
print("=" * 60)

# Read Silver data
df = pd.read_parquet(SILVER_FILE)

print("Silver records:", len(df))
print("Available columns:", list(df.columns))

# -------------------------------------------------
# Make sure numeric columns are numeric
# -------------------------------------------------

df["quantity"] = pd.to_numeric(
    df["quantity"],
    errors="coerce"
)

df["unit_price"] = pd.to_numeric(
    df["unit_price"],
    errors="coerce"
)

df["total_amount"] = pd.to_numeric(
    df["total_amount"],
    errors="coerce"
)

# -------------------------------------------------
# 1. Overall Summary
# -------------------------------------------------

summary = pd.DataFrame({
    "metric": [
        "Total Revenue",
        "Total Quantity Sold",
        "Total Transactions",
        "Average Order Value"
    ],
    "value": [
        round(df["total_amount"].sum(), 2),
        df["quantity"].sum(),
        df["transaction_id"].nunique(),
        round(df["total_amount"].mean(), 2)
    ]
})

summary.to_csv(
    f"{GOLD_DIR}/summary.csv",
    index=False
)

# -------------------------------------------------
# 2. Sales by Region
# -------------------------------------------------

region_sales = (
    df.groupby("region")
    .agg(
        total_sales=("total_amount", "sum"),
        total_quantity=("quantity", "sum"),
        transactions=("transaction_id", "nunique")
    )
    .reset_index()
    .sort_values("total_sales", ascending=False)
)

region_sales["total_sales"] = region_sales["total_sales"].round(2)

region_sales.to_csv(
    f"{GOLD_DIR}/sales_by_region.csv",
    index=False
)

# -------------------------------------------------
# 3. Sales by Store
# -------------------------------------------------

store_sales = (
    df.groupby("store_id")
    .agg(
        total_sales=("total_amount", "sum"),
        total_quantity=("quantity", "sum"),
        transactions=("transaction_id", "nunique")
    )
    .reset_index()
    .sort_values("total_sales", ascending=False)
)

store_sales["total_sales"] = store_sales["total_sales"].round(2)

store_sales.to_csv(
    f"{GOLD_DIR}/sales_by_store.csv",
    index=False
)

# -------------------------------------------------
# 4. Top 10 Products
# -------------------------------------------------

top_products = (
    df.groupby("sku")
    .agg(
        total_sales=("total_amount", "sum"),
        quantity_sold=("quantity", "sum")
    )
    .reset_index()
    .sort_values("total_sales", ascending=False)
    .head(10)
)

top_products["total_sales"] = top_products["total_sales"].round(2)

top_products.to_csv(
    f"{GOLD_DIR}/top_products.csv",
    index=False
)

# -------------------------------------------------
# 5. Daily Sales
# -------------------------------------------------

date_column_found = False

if "event_datetime" in df.columns:

    df["event_datetime"] = pd.to_datetime(
        df["event_datetime"],
        errors="coerce"
    )

    df["date"] = df["event_datetime"].dt.date

    date_column_found = True

elif "event_timestamp" in df.columns:

    # Timestamp is assumed to be milliseconds
    df["event_timestamp"] = pd.to_numeric(
        df["event_timestamp"],
        errors="coerce"
    )

    df["date"] = pd.to_datetime(
        df["event_timestamp"],
        unit="ms",
        errors="coerce"
    ).dt.date

    date_column_found = True


if date_column_found:

    daily_sales = (
        df.dropna(subset=["date"])
        .groupby("date")
        .agg(
            total_sales=("total_amount", "sum"),
            quantity_sold=("quantity", "sum"),
            transactions=("transaction_id", "nunique")
        )
        .reset_index()
    )

    daily_sales["total_sales"] = daily_sales[
        "total_sales"
    ].round(2)

    daily_sales.to_csv(
        f"{GOLD_DIR}/daily_sales.csv",
        index=False
    )

else:

    print("WARNING: No timestamp column found.")
    print("Daily sales file will not be created.")

# -------------------------------------------------
# Display Results
# -------------------------------------------------

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print(summary.to_string(index=False))

print("\n" + "=" * 60)
print("SALES BY REGION")
print("=" * 60)

print(region_sales.to_string(index=False))

print("\n" + "=" * 60)
print("TOP PRODUCTS")
print("=" * 60)

print(top_products.to_string(index=False))

# -------------------------------------------------
# Finished
# -------------------------------------------------

print("\n" + "=" * 60)
print("GOLD LAYER CREATED SUCCESSFULLY")
print("=" * 60)

print("\nFiles created:")

for file in sorted(os.listdir(GOLD_DIR)):
    print(" -", file)
