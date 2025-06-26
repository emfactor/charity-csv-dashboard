import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Charity Dashboard", layout="wide")

st.title("📊 Charity Donation Dashboard")

# Load CSV
df = pd.read_csv("sample_charity_data.csv")

# 🔧 Convert 'Date' to datetime
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# Sidebar filters
campaign = st.sidebar.selectbox("Select Campaign", ["All"] + sorted(df["Campaign"].unique().tolist()))
if campaign != "All":
    df = df[df["Campaign"] == campaign]

# Summary stats
total = df["Amount"].sum()
donations = df.shape[0]
avg = df["Amount"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Raised", f"£{total:,.2f}")
col2.metric("🧾 # of Donations", donations)
col3.metric("📊 Avg Donation", f"£{avg:,.2f}")

# Chart
monthly = df.groupby("Month")["Amount"].sum().reset_index()
fig = px.bar(monthly, x="Month", y="Amount", title="Monthly Donation Totals", labels={"Amount": "£ Amount"})
st.plotly_chart(fig, use_container_width=True)

# Table
st.subheader("📋 Raw Donation Data")
st.dataframe(df.sort_values("Date", ascending=False))
