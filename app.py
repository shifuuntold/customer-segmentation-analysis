import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

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

st.subheader("🏆 Top Customer Insights")

top_customer_value = filtered_df["Monetary"].max()

top_1_customer = filtered_df.sort_values("Monetary", ascending=False).iloc[0]

st.metric(
    label="Top Customer Revenue",
    value=f"${top_customer_value:,.0f}"
)

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

top_10_pct = int(len(filtered_df) * 0.1)

top_10_revenue_share = (
    filtered_df.sort_values("Monetary", ascending=False)
    .head(top_10_pct)["Monetary"].sum()
    / filtered_df["Monetary"].sum()
    * 100
)

st.metric(
    label="Top 10% Revenue Contribution",
    value=f"{top_10_revenue_share:.1f}%"
)

st.divider()

# Segment Distribution
st.subheader("Customer Segment Distribution")

segment_counts = filtered_df["Segment"].value_counts()

if not segment_counts.empty:
    fig1 = px.bar(
        x=segment_counts.index,
        y=segment_counts.values,
        labels={"x": "Segment", "y": "Customers"},
        title="Customer Segment Distribution"
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("No data available for selected filters.")

fig1 = px.bar(
    x=segment_counts.index,
    y=segment_counts.values,
    labels={"x": "Segment", "y": "Customers"},
    title="Customer Segment Distribution"
)

st.plotly_chart(fig1, use_container_width=True)

# Monetary Distribution
st.subheader("Customer Spending Distribution")

fig2 = px.histogram(
    filtered_df,
    x="Monetary",
    nbins=30,
    title="Customer Spending Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# Top Customers
st.subheader("Top 20 Customers")

top_customers = (
    filtered_df
    .sort_values("Monetary", ascending=False)
    .head(20)
)

st.dataframe(top_customers)

st.download_button(
    label="📥 Download Filtered Customers",
    data=filtered_df.to_csv(index=False),
    file_name="rfm_segment.csv",
    mime="text/csv"
)

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