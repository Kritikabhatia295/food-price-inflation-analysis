
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Food Price and Inflation Analysis",
    layout="wide"
)

st.title("Food Price and Inflation Analysis - India")
st.write("Search food commodities and explore price trends and predictions.")

df = pd.read_csv("food_prices.csv")

df.columns = df.columns.str.strip().str.lower()
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")

df = df.dropna(subset=["date", "commodity", "price"])
df["commodity"] = df["commodity"].astype(str).str.strip()

st.subheader("Search Food Commodity")

search = st.text_input(
    "Enter food item name",
    placeholder="Example: Rice, Wheat, Tomato, Onion..."
)

commodities = sorted(df["commodity"].unique())

if search:
    matches = [
        item for item in commodities
        if search.lower() in item.lower()
    ]

    if matches:
        days = st.selectbox(
            "Prediction period",
            [30, 90, 180, 365]
        )

        for item in matches:
            data = df[
                df["commodity"].str.lower() == item.lower()
            ].copy()

            data = data.sort_values("date")

            st.header(item)

            st.line_chart(
                data.set_index("date")[["price"]]
            )

            col1, col2, col3 = st.columns(3)

            col1.metric("Average Price", round(data["price"].mean(), 2))
            col2.metric("Minimum Price", round(data["price"].min(), 2))
            col3.metric("Maximum Price", round(data["price"].max(), 2))

            if len(data) >= 2:
                data["days"] = (
                    data["date"] - data["date"].min()
                ).dt.days

                x = data["days"].to_numpy(dtype=float)
                y = data["price"].to_numpy(dtype=float)

                slope, intercept = np.polyfit(x, y, 1)

                future_day = x.max() + days
                prediction = slope * future_day + intercept

                st.success(
                    f"Estimated price after {days} days: "
                    f"{prediction:.2f}"
                )
            else:
                st.warning("Not enough data for prediction.")

            st.dataframe(data, use_container_width=True)
            st.divider()

    else:
        st.warning("No matching food item found.")

else:
    st.info("Type a food item name to search.")
    st.write("Available commodities:", ", ".join(commodities))
