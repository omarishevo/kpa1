import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.express as px

# Page configuration
st.set_page_config(page_title="KPA Cargo Forecast", layout="wide")
st.title("📦 Kenya Ports Authority - Cargo Volume Forecasting")

# File uploader
uploaded_file = st.file_uploader("Upload CSV with 'Date' and 'CargoVolume' columns", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.subheader("📊 Raw Data Preview")
        st.dataframe(df.head())

        # Validate required columns
        if 'Date' not in df.columns or 'CargoVolume' not in df.columns:
            st.error("Dataset must contain 'Date' and 'CargoVolume' columns.")
        else:
            # Convert date column
            df['Date'] = pd.to_datetime(df['Date'])

            # Rename columns for Prophet
            df_prophet = df.rename(columns={'Date': 'ds', 'CargoVolume': 'y'})

            # Plot historical data
            st.subheader("📈 Historical Cargo Volume")
            fig = px.line(df, x='Date', y='CargoVolume', title="Cargo Volume Over Time")
            st.plotly_chart(fig)

            # Forecast settings
            st.subheader("🔮 Forecast Settings")
            periods = st.slider("Months to Forecast", min_value=1, max_value=24, value=6)

            # Train Prophet model
            model = Prophet()
            model.fit(df_prophet)

            # Create future dataframe
            future = model.make_future_dataframe(periods=periods * 30)  # Approximate by 30 days/month
            forecast = model.predict(future)

            # Plot forecast
            st.subheader("📈 Forecast Plot")
            forecast_fig = plot_plotly(model, forecast)
            st.plotly_chart(forecast_fig)

            # Forecast table
            st.subheader("📉 Forecast Table")
            forecast_filtered = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods * 30)
            st.dataframe(forecast_filtered)

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")

else:
    st.info("Please upload a CSV file with at least two columns: 'Date' and 'CargoVolume'.")
