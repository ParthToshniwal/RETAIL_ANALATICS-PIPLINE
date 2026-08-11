import streamlit as st
import pandas as pd
import os

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Retail Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GOLD_DIR = os.path.join(
    BASE_DIR,
    "landing",
    "gold"
)

# --------------------------------------------------
# Load data
# --------------------------------------------------

summary = pd.read_csv(
    os.path.join(GOLD_DIR, "summary.csv")
)

region_sales = pd.read_csv(
    os.path.join(GOLD_DIR, "sales_by_region.csv")
)

store_sales = pd.read_csv(
    os.path.join(GOLD_DIR, "sales_by_store.csv")
)

top_products = pd.read_csv(
    os.path.join(GOLD_DIR, "top_products.csv")
)

daily_sales_file = os.path.join(
    GOLD_DIR,
    "daily_sales.csv"
)

if os.path.exists(daily_sales_file):
    daily_sales = pd.read_csv(daily_sales_file)
else:
    daily_sales = pd.DataFrame()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🛒 Retail Analytics Dashboard")

st.markdown(
    "### Real-Time Retail Transaction Analytics"
)

st.markdown("---")

# --------------------------------------------------
# Get summary values
# --------------------------------------------------

def get_metric(metric_name):

    row = summary[
        summary["metric"] == metric_name
    ]

    if len(row) > 0:
        return row.iloc[0]["value"]

    return 0


total_revenue = get_metric(
    "Total Revenue"
)

total_quantity = get_metric(
    "Total Quantity Sold"
)

total_transactions = get_metric(
    "Total Transactions"
)

average_order = get_metric(
    "Average Order Value"
)

# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"₹{total_revenue:,.2f}"
    )

with col2:
    st.metric(
        "🛒 Transactions",
        f"{int(total_transactions):,}"
    )

with col3:
    st.metric(
        "📦 Quantity Sold",
        f"{int(total_quantity):,}"
    )

with col4:
    st.metric(
        "📊 Average Order",
        f"₹{average_order:,.2f}"
    )

st.markdown("---")

# --------------------------------------------------
# Sales by Region
# --------------------------------------------------

st.subheader("🌍 Sales by Region")

if not region_sales.empty:

    st.bar_chart(
        region_sales.set_index("region")[
            "total_sales"
        ]
    )

    st.dataframe(
        region_sales,
        use_container_width=True
    )

# --------------------------------------------------
# Store + Products
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏪 Sales by Store")

    if not store_sales.empty:

        st.bar_chart(
            store_sales.set_index("store_id")[
                "total_sales"
            ].head(15)
        )

with col2:

    st.subheader("🏆 Top 10 Products")

    if not top_products.empty:

        st.bar_chart(
            top_products.set_index("sku")[
                "total_sales"
            ]
        )

# --------------------------------------------------
# Daily Sales
# --------------------------------------------------

st.markdown("---")

st.subheader("📈 Daily Sales Trend")

if not daily_sales.empty:

    daily_sales["date"] = pd.to_datetime(
        daily_sales["date"]
    )

    daily_sales = daily_sales.sort_values(
        "date"
    )

    st.line_chart(
        daily_sales.set_index("date")[
            "total_sales"
        ]
    )

else:

    st.info(
        "Daily sales data is not available."
    )

# --------------------------------------------------
# Raw Gold Data
# --------------------------------------------------

st.markdown("---")

with st.expander("View Gold Data"):

    st.subheader("Summary")

    st.dataframe(
        summary,
        use_container_width=True
    )

    st.subheader("Region Sales")

    st.dataframe(
        region_sales,
        use_container_width=True
    )

    st.subheader("Store Sales")

    st.dataframe(
        store_sales,
        use_container_width=True
    )

    st.subheader("Top Products")

    st.dataframe(
        top_products,
        use_container_width=True
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Retail Analytics Platform | "
    "Kafka + Python + Pandas + Parquet + Streamlit"
)
