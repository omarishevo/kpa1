import streamlit as st
import pandas as pd

st.set_page_config(page_title="KPA Personnel Dashboard", layout="wide")
st.title("Kenya Ports Authority (KPA) Personnel Dashboard")

uploaded_file = st.file_uploader("Upload the KPA personnel CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    st.sidebar.header("🔎 Filter Data (Only from Columns Present)")

    filters = []

    # Auto-select categorical columns for filtering
    filterable_columns = [
        col for col in df.columns
        if df[col].dtype == 'object' or df[col].nunique() <= 30
    ]

    for col in filterable_columns:
        options = df[col].dropna().unique().tolist()
        selected = st.sidebar.multiselect(f"Filter by {col}", options, default=options)
        filters.append(df[col].isin(selected))

    # Apply filters
    if filters:
        combined_filter = filters[0]
        for f in filters[1:]:
            combined_filter &= f
        filtered_df = df[combined_filter]
    else:
        filtered_df = df.copy()

    st.subheader(f"🔍 Filtered Results ({len(filtered_df)} records)")
    st.dataframe(filtered_df)

    st.subheader("📊 Summary Charts")

    # Chart only if column exists in filtered_df
    for col in filterable_columns:
        if col in filtered_df.columns and not filtered_df[col].empty:
            st.markdown(f"**Count by {col}**")
            st.bar_chart(filtered_df[col].value_counts())

else:
    st.warning("📂 Please upload the `kpa_personnel_dataset_final.csv` file to begin.")
