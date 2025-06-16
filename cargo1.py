import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go

# Page setup
st.set_page_config(page_title="KPA Cargo Forecast", layout="wide")
st.title("📦 Kenya Ports Authority - Cargo Volume Forecasting")

# File upload
uploaded_file = st.file_uploader("Upload CSV with cargo data (Date & CargoVolume columns)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Raw Data Preview")
    st.dataframe(df.head())

    if 'Date' not in df.columns or 'CargoVolume' not in df.columns:
        st.error("Dataset must contain '
