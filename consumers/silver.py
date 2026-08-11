import pandas as pd
import os
import glob

BRONZE_DIR = "landing/bronze"
SILVER_DIR = "landing/silver"

os.makedirs(SILVER_DIR, exist_ok=True)

files = glob.glob(BRONZE_DIR + "/*.json")

if not files:
    print("No Bronze data found.")
    exit()

data = []

for file in files:
    with open(file, "r") as f:
        for line in f:
            if line.strip():
                data.append(eval(line.strip()))

df = pd.DataFrame(data)

print("Bronze records:", len(df))

# Clean data
df = df.dropna(subset=[
    "transaction_id",
    "store_id",
    "sku"
])

df["quantity"] = pd.to_numeric(
    df["quantity"],
    errors="coerce"
)

df["unit_price"] = pd.to_numeric(
    df["unit_price"],
    errors="coerce"
)

df = df[
    (df["quantity"] > 0) &
    (df["unit_price"] >= 0)
]

# Remove duplicates
df = df.drop_duplicates(
    subset=["transaction_id"]
)

# Calculate sales
df["total_amount"] = (
    df["quantity"] * df["unit_price"]
).round(2)

# Clean strings
df["store_id"] = df["store_id"].str.upper().str.strip()
df["region"] = df["region"].str.upper().str.strip()
df["sku"] = df["sku"].str.upper().str.strip()

# Save Silver
output = f"{SILVER_DIR}/transactions.parquet"

df.to_parquet(
    output,
    index=False
)

print("=" * 60)
print("SILVER CREATED SUCCESSFULLY")
print("=" * 60)

print("Silver records:", len(df))
print("File:", output)

print(df.head())
