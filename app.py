import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load Data
df = pd.read_csv("rfm.csv")

# Create Segment Labels
def assign_segment(score):
    score = str(score)

    if score.startswith("44") or score.startswith("43"):
        return "Champions"
    elif score.startswith("34") or score.startswith("33"):
        return "Loyal Customers"
    elif score.startswith("24") or score.startswith("23"):
        return "Potential Loyalists"
    elif score.startswith("14") or score.startswith("13"):
        return "At Risk"
    else:
        return "Others"

df["Segment"] = df["RFM_Score"].apply(assign_segment)

# Sidebar
st.sidebar.header("Filters")

selected_segment = st.sidebar.multiselect(
    "Select Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

filtered_df = df[df["Segment"].isin(selected_segment)]

# Title
st.title("📊 Customer Segmentation Analysis Dashboard")
st.markdown("RFM-Based Customer Segmentation Analysis")

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Customers",
    f"{len(filtered_df):,}"
)

col2.metric(
    "Revenue",
    f"${filtered_df['Monetary'].sum():,.0f}"
)

col3.metric(
    "Avg Revenue",
    f"${filtered_df['Monetary'].mean():,.0f}"
)

col4.metric(
    "Highest Customer Value",
    f"${filtered_df['Monetary'].max():,.0f}"
)

st.divider()

# Segment Distribution
st.subheader("Customer Segment Distribution")

segment_counts = (
    filtered_df["Segment"]
    .value_counts()
)

fig1, ax1 = plt.subplots(figsize=(8,4))
segment_counts.plot(
    kind="bar",
    ax=ax1
)

ax1.set_xlabel("Segment")
ax1.set_ylabel("Customers")

st.pyplot(fig1)

# Monetary Distribution
st.subheader("Customer Spending Distribution")

fig2, ax2 = plt.subplots(figsize=(8,4))

ax2.hist(
    filtered_df["Monetary"],
    bins=30
)

ax2.set_xlabel("Monetary Value")
ax2.set_ylabel("Frequency")

st.pyplot(fig2)

# Top Customers
st.subheader("Top 20 Customers")

top_customers = (
    filtered_df
    .sort_values("Monetary", ascending=False)
    .head(20)
)

st.dataframe(top_customers)

# Summary
st.subheader("Key Insights")

top_15_pct = int(len(filtered_df) * 0.15)

top_revenue_share = (
    filtered_df
    .sort_values("Monetary", ascending=False)
    .head(top_15_pct)["Monetary"]
    .sum()
    /
    filtered_df["Monetary"].sum()
    * 100
)

st.success(
    f"Top 15% customers contribute approximately "
    f"{top_revenue_share:.1f}% of total revenue."
)