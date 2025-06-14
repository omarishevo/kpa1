import streamlit as st
import pandas as pd

st.set_page_config(page_title="KPA Personnel Dashboard", layout="wide")

st.title("Kenya Ports Authority (KPA) Personnel Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload the KPA personnel CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    # Sidebar filters
    st.sidebar.header("🔎 Filter Personnel Data")
    
    # Dynamic filters
    position_options = df['Position'].dropna().unique().tolist()
    selected_position = st.sidebar.multiselect("Filter by Position", position_options, default=position_options)

    department_options = df['Department'].dropna().unique().tolist() if 'Department' in df.columns else []
    selected_department = st.sidebar.multiselect("Filter by Department", department_options, default=department_options)

    gender_options = df['Gender'].dropna().unique().tolist() if 'Gender' in df.columns else []
    selected_gender = st.sidebar.multiselect("Filter by Gender", gender_options, default=gender_options)

    # Apply filters
    filtered_df = df[
        (df['Position'].isin(selected_position)) &
        (df['Department'].isin(selected_department) if 'Department' in df.columns else True) &
        (df['Gender'].isin(selected_gender) if 'Gender' in df.columns else True)
    ]

    st.subheader(f"🔍 Filtered Results ({len(filtered_df)} records
