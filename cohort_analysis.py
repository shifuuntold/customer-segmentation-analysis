import pandas as pd

# Load data
df = pd.read_csv("rfm.csv")

# Clean CustomerID (VERY IMPORTANT)
df = df.dropna(subset=["CustomerID"])
df["CustomerID"] = df["CustomerID"].astype(int)

# Convert dates
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Create invoice month
df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M")

# Cohort month (first purchase)
df["CohortMonth"] = df.groupby("CustomerID")["InvoiceMonth"].transform("min")

# Function to calculate cohort index
def get_month_diff(row):
    return (row["InvoiceMonth"].year - row["CohortMonth"].year) * 12 + \
           (row["InvoiceMonth"].month - row["CohortMonth"].month)

df["CohortIndex"] = df.apply(get_month_diff, axis=1)

# Cohort table (retention view)
cohort_data = df.groupby(["CohortMonth", "CohortIndex"])["CustomerID"].nunique().reset_index()

print(cohort_data.head())