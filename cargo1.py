import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="KPA Cargo Forecast", layout="wide")
st.title("📦 Kenya Ports Authority - Cargo Volume Forecasting")

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV with 'Date' and 'CargoVolume' columns", type="csv")

if uploaded_file is not None:
    try:
        # Load data
        df = pd.read_csv(uploaded_file)

        st.subheader("📊 Raw Data Preview")
        st.dataframe(df.head())

        # Validate required columns
        if 'Date' not in df.columns or 'CargoVolume' not in df.columns:
            st.error("Dataset must contain 'Date' and 'CargoVolume' columns.")
        else:
            # Convert Date column and sort
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')

            # Historical plot
            st.subheader("📈 Historical Cargo Volume")
            fig = px.line(df, x='Date', y='CargoVolume', title="Cargo Volume Over Time")
            st.plotly_chart(fig)

            # Simple Moving Average Forecast
            st.subheader("🔮 Simple Moving Average Forecast")
            window = st.slider("Rolling Window Size (Months)", min_value=1, max_value=12, value=3)

            df['SMA_Forecast'] = df['CargoVolume'].rolling(window=window).mean()

            # Forecast plot
            fig_forecast = px.line(
                df,
                x='Date',
                y=['CargoVolume', 'SMA_Forecast'],
                labels={"value": "Volume", "variable": "Legend"},
                title="Cargo Volume with Simple Moving Average"
            )
            st.plotly_chart(fig_forecast)

            # Forecast table
            st.subheader("📉 Forecast Table (with SMA)")
            st
