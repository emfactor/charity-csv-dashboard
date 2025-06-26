import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Charity Donation Dashboard", layout="wide")

st.title("📊 Charity Donation Dashboard")

# Load data
df = pd.read_csv("sample_charity_data.csv")

# Safely convert 'Date' column to datetime, coerce errors to NaT
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

# Drop rows where 'Date' is NaT (invalid date)
df = df.dropna(subset=["Date"])

# Create a 'Month' column for grouping
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# Sidebar filter for campaigns
campaigns = ["All"] + sorted(df["Campaign"].unique().tolist())
selected_campaign = st.sidebar.selectbox("Select Campaign", campaigns)

if selected_campaign != "All":
    df = df[df["Campaign"] == selected_campaign]

# Calculate summary statistics
total_raised = df["Amount"].sum()
num_donations = df.shape[0]
avg_donation = df["Amount"].mean()

# Show metrics
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Raised", f"£{total_raised:,.2f}")
col2.metric("🧾 Number of Donations", num_donations)
col3.metric("📊 Average Donation", f"£{avg_donation:,.2f}")

# Monthly donation totals chart
monthly_totals = df.groupby("Month")["Amount"].sum().reset_index()
fig = px.bar(monthly_totals, x="Month", y="Amount", title="Monthly Donation Totals", labels={"Amount": "£ Amount"})
st.plotly_chart(fig, use_container_width=True)

# Show data table
st.subheader("📋 Donation Data")
st.dataframe(df.sort_values("Date", ascending=False))
