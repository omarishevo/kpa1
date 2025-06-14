import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.express as px
import plotly.graph_objs as go

st.set_page_config(page_title="KPA Cargo Forecast", layout="wide")
st.title("📦 Kenya Ports Authority - Cargo Volume Forecasting")

uploaded_file = st.file_uploader("Upload CSV with cargo data (Date & Volume columns)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Raw Data Preview")
    st.dataframe(df.head())

    # Ensure required columns exist
    if 'Date' not in df.columns or 'CargoVolume' not in df.columns:
        st.error("Dataset must contain 'Date' and 'CargoVolume' columns.")
    else:
        # Convert date
        df['Date'] = pd.to_datetime(df['Date'])

        # Prepare data for Prophet
        df_prophet = df.rename(columns={'Date': 'ds', 'CargoVolume': 'y'})

        st.subheader("📈 Historical Cargo Volume")
        fig = px.line(df, x='Date', y='CargoVolume', title="Cargo Volume Over Time")
        st.plotly_chart(fig)

        # Forecasting
        st.subheader("🔮 Forecast Settings")
        periods = st.slider("Months to Forecast", min_value=1, max_value=24, value=6)

        model = Prophet()
        model.fit(df_prophet)

        future = model.make_future_dataframe(periods=periods * 30)  # days
        forecast = model.predict(future)

        st.subheader("📈 Forecast Plot")
        forecast_fig = plot_plotly(model, forecast)
        st.plotly_chart(forecast_fig)

        st.subheader("📉 Forecast Table")
        st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

else:
    st.info("Please upload a CSV file with at least two columns: `Date` and `CargoVolume`.")

