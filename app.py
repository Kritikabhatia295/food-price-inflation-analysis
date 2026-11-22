
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Food Price and Inflation Analysis",
    layout="wide"
)

st.title("Food Price and Inflation Analysis – India")
st.write("Explore food prices and inflation trends using historical data.")

df = pd.read_csv("food_prices.csv")

df.columns = df.columns.str.strip().str.lower()

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")

df = df.dropna(subset=["date", "commodity", "price"])

items = sorted(df["commodity"].dropna().unique())

selected_item = st.selectbox("Select a food item", items)

filtered = df[df["commodity"] == selected_item].sort_values("date")

st.subheader(f"{selected_item} Price Trend")

chart_data = filtered.set_index("date")[["price"]]
st.line_chart(chart_data)

st.subheader("Price Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Average Price", round(filtered["price"].mean(), 2))
col2.metric("Minimum Price", round(filtered["price"].min(), 2))
col3.metric("Maximum Price", round(filtered["price"].max(), 2))

st.subheader("Dataset")
st.dataframe(filtered)

