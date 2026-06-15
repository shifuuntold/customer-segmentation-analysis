# Customer Segmentation Analysis Dashboard

## Overview

This project applies RFM (Recency, Frequency, Monetary) analysis to segment customers based on purchasing behavior and identify high-value customer groups.

Using transaction-level retail data, customers are classified into meaningful segments to support targeted marketing, retention strategies, and revenue optimization.

The project includes an interactive Streamlit dashboard for exploring customer segments, spending patterns, and business insights.

---

## Business Problem

Businesses often struggle to identify:

* Their most valuable customers
* Customers at risk of churning
* Revenue concentration among customer groups
* Opportunities for targeted marketing campaigns

This project addresses these challenges using RFM segmentation and interactive analytics.

---

## Dataset

Online Retail Dataset

* Approximately 397,000 cleaned transactions
* Customer purchase history
* Product information
* Transaction dates
* Revenue data

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Streamlit
* Jupyter Notebook
* Git
* GitHub

---

## Project Workflow

### 1. Data Cleaning

* Removed missing Customer IDs
* Removed cancelled transactions
* Removed invalid quantities and prices

### 2. Feature Engineering

Created:

* Total Transaction Value
* Recency
* Frequency
* Monetary Value

### 3. RFM Analysis

Calculated:

* Recency (days since last purchase)
* Frequency (number of purchases)
* Monetary (total customer spend)

### 4. Customer Segmentation

Customers were grouped into segments such as:

* Champions
* Loyal Customers
* Potential Loyalists
* At Risk Customers
* Others

### 5. Dashboard Development

Built an interactive Streamlit dashboard featuring:

* KPI Cards
* Customer Segment Distribution
* Spending Distribution Analysis
* Top Customer Identification
* Revenue Concentration Insights

---

## Key Findings

* Processed over 397,000 retail transactions
* Automated customer segmentation using RFM methodology
* Identified high-value customer groups responsible for a significant share of revenue
* Built an interactive analytics dashboard for business decision-making

---

## Dashboard Features

### KPI Monitoring

* Total Customers
* Total Revenue
* Average Customer Revenue
* Highest Customer Value

### Interactive Filters

* Segment-based filtering

### Visualizations

* Customer Segment Distribution
* Customer Spending Distribution

### Customer Insights

* Top 20 Customers
* Revenue Contribution Analysis

---

## Project Structure

Customer-Segmentation-Analysis/

├── app.py

├── rfm.csv

├── requirements.txt

├── data/

│   └── Online_Retail.xlsx

├── notebooks/

│   └── RFM_Build.ipynb

└── README.md

---

## How to Run Locally

1. Clone the repository

git clone https://github.com/shifuuntold/customer-segmentation-analysis.git

2. Navigate to the project folder

cd customer-segmentation-analysis

3. Install dependencies

pip install -r requirements.txt

4. Run the dashboard

streamlit run app.py

---

## Future Improvements

* Customer Lifetime Value (CLV) Prediction
* Advanced Segmentation Models
* Interactive Plotly Visualizations
* Marketing Campaign Recommendations
* Churn Prediction Models

---

## Author

Ramon

Business Information Technology (BBIT)

Data Analytics | Business Intelligence | Customer Analytics
