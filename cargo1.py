import streamlit as st
import pandas as pdimport streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("kpa_personnel_dataset_final.csv")

df = load_data()

# Page setup
st.set_page_config(page_title="KPA Personnel Dashboard", layout="wide")
st.title("👷 Kenya Ports Authority - Personnel Analysis")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
roles = st.sidebar.multiselect("Select Role", options=df["Role"].unique(), default=df["Role"].unique())
locations = st.sidebar.multiselect("Select Work Location", options=df["Work Location"].unique(), default=df["Work Location"].unique())
companies = st.sidebar.multiselect("Select Company", options=df["Company"].unique(), default=df["Company"].unique())

filtered_df = df[
    (df["Role"].isin(roles)) &
    (df["Work Location"].isin(locations)) &
    (df["Company"].isin(companies))
]

# Show filtered data
st.subheader("📋 Filtered Personnel Data")
st.dataframe(filtered_df)

# Years of experience distribution
st.subheader("📊 Years of Experience Distribution")
fig_exp = px.histogram(filtered_df, x="Years of Experience", nbins=15, color="Shift", title="Experience by Shift")
st.plotly_chart(fig_exp)

# Staff per Work Location
st.subheader("🏢 Staff Count per Work Location")
fig_loc = px.bar(filtered_df['Work Location'].value_counts().reset_index(),
                 x='index', y='Work Location', labels={'index': 'Location', 'Work Location': 'Number of Staff'},
                 color='index')
st.plotly_chart(fig_loc)

# Shift distribution
st.subheader("🕒 Shift Distribution")
fig_shift = px.pie(filtered_df, names='Shift', title="Distribution by Shift")
st.plotly_chart(fig_shift)

# Gate usage
st.subheader("🚪 Most Used Gates")
fig_gate = px.bar(filtered_df['Mostly Used Gate'].value_counts().reset_index(),
                  x='index', y='Mostly Used Gate',
                  labels={'index': 'Gate', 'Mostly Used Gate': 'Number of Users'})
st.plotly_chart(fig_gate)

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
