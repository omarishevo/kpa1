import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="KPA Personnel Dashboard", layout="wide")

st.title("Kenya Ports Authority (KPA) Personnel Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload the KPA personnel CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Show preview
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    # Sidebar filters
    st.sidebar.header("🔎 Filter Personnel Data")
    
    # Dynamic filters based on existing columns
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

    # Show filtered data
    st.subheader(f"🔍 Filtered Results ({len(filtered_df)} records)")
    st.dataframe(filtered_df)

    # Visualizations
    st.subheader("📊 Visualization")

    col1, col2 = st.columns(2)

    with col1:
        if 'Position' in df.columns:
            fig1 = px.histogram(filtered_df, x='Position', title='Personnel Count by Position')
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        if 'Department' in df.columns:
            fig2 = px.histogram(filtered_df, x='Department', title='Personnel Count by Department')
            st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("Please upload the `kpa_personnel_dataset_final.csv` file to proceed.")
