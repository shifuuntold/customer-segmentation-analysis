import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from report_generator import generate_report

# Page Config
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

[data-testid="metric-container"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 10px;
}

[data-testid="metric-container"] label {
    color: white;
}

[data-testid="metric-container"] div {
    color: white;
}
</style>
""", unsafe_allow_html=True)

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

default_segments = df["Segment"].unique()

# Use multiselect return value and explicit defaults instead of direct session-state reads
# (removed manual session_state management for selected_segment to improve readability/testability)

selected_segment = st.sidebar.multiselect(
    "Select Segment",
    options=df["Segment"].unique(),
    default=list(default_segments)
)

filtered_df = df[df["Segment"].isin(selected_segment)]

top_15_pct = max(1, int(len(filtered_df) * 0.15))

top_revenue_share = (
    filtered_df
    .sort_values("Monetary", ascending=False)
    .head(top_15_pct)["Monetary"]
    .sum()
    /
    filtered_df["Monetary"].sum()
    * 100
)

# Title
st.title("📊 Customer Segmentation Dashboard")

with st.container():
    st.caption("Executive Customer Insights (RFM Analysis)")
    st.write("This dashboard analyzes customer behavior using RFM segmentation.")
if filtered_df.empty:
    st.info("No customers match the selected filters. Try adjusting your segment selection.")
    st.stop()

st.markdown("---")

# KPIs
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

customers = len(filtered_df)
revenue = filtered_df["Monetary"].sum()
avg_rev = filtered_df["Monetary"].mean()
max_rev = filtered_df["Monetary"].max()

col1.metric("👥 Customers", f"{customers:,}")
col2.metric("💰 Revenue", f"${revenue:,.0f}")
col3.metric("📊 Avg Revenue", f"${avg_rev:,.0f}")
col4.metric("🏆 Top Customer", f"${max_rev:,.0f}")

st.subheader("🧠 Customer Personas Overview")

champions = filtered_df[filtered_df["Segment"] == "Champions"]
loyal = filtered_df[filtered_df["Segment"] == "Loyal Customers"]
at_risk = filtered_df[filtered_df["Segment"] == "At Risk"]

c1, c2, c3 = st.columns(3)

c1.metric("🔥 Champions", len(champions))
c2.metric("💎 Loyal Customers", len(loyal))
c3.metric("⚠️ At Risk", len(at_risk))

st.subheader("🏆 Top Customer Insights")

top_customer_value = filtered_df["Monetary"].max()

top_1_customer = filtered_df.sort_values("Monetary", ascending=False).iloc[0]

st.metric(
    label="Top Customer Revenue",
    value=f"${top_customer_value:,.0f}"
)

st.subheader("📈 Revenue Concentration Insight")

if filtered_df["Monetary"].sum() > 0:
    top_n = max(1, int(len(filtered_df) * 0.1))

    top_share = (
        filtered_df.sort_values("Monetary", ascending=False)
        .head(top_n)["Monetary"].sum()
        / filtered_df["Monetary"].sum()
        * 100
    )

    st.success(f"Top 10% of customers generate {top_share:.1f}% of revenue.")
else:
    st.warning("No revenue data available for selected filters.")

st.metric(
    label="Top 10% Revenue Contribution",
    value=f"{top_share:.1f}%"
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

st.divider()

# Monetary Distribution
st.subheader("Customer Spending Distribution")

if not filtered_df.empty:
    fig2 = px.histogram(
        filtered_df,
        x="Monetary",
        nbins=30,
        title="Customer Spending Distribution"
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No data available for selected filters.")

st.divider()

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

pdf_file = generate_report(
    len(filtered_df),
    filtered_df["Monetary"].sum(),
    filtered_df["Monetary"].mean(),
    top_share
)

with open(pdf_file, "rb") as file:
    st.download_button(
        label="📄 Download Executive PDF",
        data=file,
        file_name="Executive_Report.pdf",
        mime="application/pdf"
    )

st.divider()

# Summary
st.subheader("Key Insights")

st.success(
    f"Top 15% customers contribute approximately "
    f"{top_revenue_share:.1f}% of total revenue."
)