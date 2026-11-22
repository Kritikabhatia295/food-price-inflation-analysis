

import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Food Price and Inflation Analysis",
    layout="wide"
)

st.title("Food Price and Inflation Analysis - India")
st.write("Analysis and future price predictions for all food commodities.")

df = pd.read_csv("food_prices.csv")

df.columns = df.columns.str.strip().str.lower()
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")

df = df.dropna(subset=["date", "commodity", "price"])
df["commodity"] = df["commodity"].astype(str).str.strip()

# Overall dataset
st.subheader("Food Price Dataset")
st.dataframe(df, use_container_width=True)

# Overall summary
st.subheader("Overall Price Summary")

summary = df.groupby("commodity")["price"].agg(
    ["mean", "min", "max"]
).round(2)

summary.columns = ["Average Price", "Minimum Price", "Maximum Price"]

st.dataframe(summary, use_container_width=True)

# Prediction period
days = st.selectbox(
    "Select prediction period",
    [30, 90, 180, 365]
)

# Charts and predictions for all commodities
st.subheader("Price Trends and Predictions")

for item in sorted(df["commodity"].unique()):

    data = df[df["commodity"] == item].copy()
    data = data.sort_values("date")

    st.markdown(f"### {item}")

    chart_data = data.set_index("date")[["price"]]
    st.line_chart(chart_data)

    if len(data) >= 2:

        data["days"] = (
            data["date"] - data["date"].min()
        ).dt.days

        X = data[["days"]]
        y = data["price"]

        model = LinearRegression()
        model.fit(X, y)

        future_days = data["days"].max() + days

        prediction = model.predict(
            pd.DataFrame({"days": [future_days]})
        )[0]

        st.metric(
            f"Predicted price after {days} days",
            f"{prediction:.2f}"
        )

    else:
        st.write("Not enough historical data for prediction.")

    st.divider()

st.caption(
    "Predictions are based on a simple Linear Regression trend "
    "and are illustrative, not validated economic forecasts."
)
