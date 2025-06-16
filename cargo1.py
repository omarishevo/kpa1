import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Set up the page
st.set_page_config(page_title="KPA Cargo Forecast", layout="wide")
st.title("📦 Kenya Ports Authority - Cargo Volume Forecasting")

# File uploader
uploaded_file = st.file_uploader("Upload CSV with cargo data (Date & CargoVolume columns)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Raw Data Preview")
    st.dataframe(df.head())

    # Check required columns
    if 'Date' not in df.columns or 'CargoVolume' not in df.columns:
        st.error("Dataset must contain 'Date' and 'CargoVolume' columns.")
    else:
        try:
            # Convert to datetime and sort
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')

            # Historical plot
            st.subheader("📈 Historical Cargo Volume")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df['Date'], df['CargoVolume'], label='Actual Volume')
            ax.set_title("Cargo Volume Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Cargo Volume")
            ax.grid(True)
            ax.legend()
            st.pyplot
