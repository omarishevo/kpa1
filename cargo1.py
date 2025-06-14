import streamlit as st
import pandas as pd

# Set Streamlit config
st.set_page_config(page_title="KPA Personnel Dashboard", layout="wide")
st.title("Kenya Ports Authority (KPA) Personnel Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload the KPA personnel CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    st.sidebar.header("🔎 Filter Data (Only from Columns Present)")

    filters = []
    filter_labels = []

    # Auto-detect categorical columns for filtering
    for column in df.columns:
        if df[column].dtype == 'object' or df[column].nunique() < 30:
            options = df[column].dropna().unique().tolist()
            selected = st.sidebar.multiselect(f"Filter by {column}", options, default=options)
            filters.append(df[column].isin(selected))
            filter_labels.append(column)

    # Apply filters safely
    if filters:
        combined_filter = filters[0]
        for f in filters[1:]:
            combined_filter &= f
        filtered_df = df[combined_filter]
    else:
        filtered_df = df.copy()

    st.subheader(f"🔍 Filtered Results ({len(filtered_df)} records)")
    st.dataframe(filtered_df)

    # Summary charts for all categorical columns with few unique values
    st.subheader("📊 Summary Charts")
    for column in df.columns:
        if df[column].dtype == 'object' or df[column].nunique() < 20:
            st.markdown(f"**Count by {column}**")
            st.bar_chart(filtered_df[column].value_counts())

else:
    st.warning("📂 Please upload the `kpa_personnel_dataset_final.csv` file to begin.")
