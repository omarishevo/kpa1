import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go

# Set page config
st.set_page_config(page_title="KPA Cargo Forecast", layout="wide")
st.title("📦 Kenya Ports Authority - Cargo Volume Forecasting")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV with cargo data (Date & CargoVolume columns)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Raw Data Preview")
    st.dataframe(df.head())

    # Validate columns
    if 'Date' not in df.columns or 'CargoVolume' not in df.columns:
        st.error("Dataset must contain 'Date' and 'CargoVolume' columns.")
    else:
        try:
            # Convert and sort
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')

            # Historical plot
            st.subheader("📈 Historical Cargo Volume")
            fig = px.line(df, x='Date', y='CargoVolume', title="Cargo Volume Over Time")
            st.plotly_chart(fig)

            # Moving Average Forecast
            st.subheader("🔮 Forecast using Simple Moving Average")
            window = st.slider("Smoothing Window (in months)", min_value=1, max_value=12, value=3)
            df['SMA'] = df['CargoVolume'].rolling(window=window).mean()

            #
