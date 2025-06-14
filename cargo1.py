import streamlit as st
import pandas as pd

# Streamlit app configuration
st.set_page_config(page_title="KPA Personnel Dashboard", layout="wide")

# App title
st.title("Kenya Ports Authority (KPA) Personnel Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("Upload the KPA personnel CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV
    df = pd.read_csv(uploaded_file)

    # Show the first few rows
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    # Sidebar filter options
    st.sidebar.header("🔎 Filter Personnel Data")
    
    # Position filter
    if 'Position' in df.columns:
        position_options = df['Position'].dropna().unique().tolist()
        selected_position = st.sidebar.multiselect("Filter by Position", position_options, default=position_options)
    else:
        selected_position = []

    # Department filter
    if 'Department' in df.columns:
        department_options = df['Department'].dropna().unique().tolist()
        selected_department = st.sidebar.multiselect("Filter by Department", department_options, default=department_options)
    else:
        selected_department = []

    # Gender filter (if present)
    if 'Gender' in df.columns:
        gender_options = df['Gender'].dropna().unique().tolist()
        selected_gender = st.sidebar.multiselect("Filter by Gender", gender_options, default=gender_options)
    else:
        selected_gender = []

    # Apply filters to DataFrame
    filtered_df = df[
        (df['Position'].isin(selected_position) if 'Position' in df.columns else True) &
        (df['Department'].isin(selected_department) if 'Department' in df.columns else True) &
        (df['Gender'].isin(selected_gender) if 'Gender' in df.columns else True)
    ]

    # Show filtered data
    st.subheader(f"🔍 Filtered Results ({len(filtered_df)} records)")
    st.dataframe(filtered_df)

    # Visualization with bar charts
    st.subheader("📊 Summary Charts")

    if 'Position' in df.columns:
        st.markdown("**Personnel Count by Position**")
        position_counts = filtered_df['Position'].value_counts()
        st.bar_chart(position_counts)

    if 'Department' in df.columns:
        st.markdown("**Personnel Count by Department**")
        department_counts = filtered_df['Department'].value_counts()
        st.bar_chart(department_counts)

else:
    st.warning("📂 Please upload the `kpa_personnel_dataset_final.csv` file to begin.")
