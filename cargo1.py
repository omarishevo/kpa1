import pandas as pd
import streamlit as st

# ----------------------------
# Streamlit App Configuration
# ----------------------------
st.set_page_config(
    page_title="KPA Cargo Forecast",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Title and Instructions
# ----------------------------
st.title("📦 Kenya Ports Authority - Cargo Volume Forecasting Dashboard")
st.markdown("""
This application allows you to upload and visualize cargo volume data for forecasting purposes.
Please ensure your CSV file contains at least two columns:
- **Date** (in a recognizable date format like YYYY-MM-DD)
- **CargoVolume** (numerical values representing cargo volume per date)

---
""")

# ----------------------------
# File Uploader
# ----------------------------
uploaded_file = st.file_uploader(
    label="📁 Upload a CSV file with your cargo data",
    type="csv",
    help="Ensure your CSV has 'Date' and 'CargoVolume' columns."
)

# ----------------------------
# Data Handling and Validation
# ----------------------------
if uploaded_file is not None:
    try:
        # Read the uploaded CSV file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Display raw data
        st.subheader("📊 Raw Data Preview")
        st.dataframe(df.head(10), use_container_width=True)

        # Check for required columns
        if 'Date' not in df.columns or 'CargoVolume' not in df.columns:
            st.error("❌ The uploaded CSV must contain 'Date' and 'CargoVolume' columns.")
        else:
            # Try to convert the 'Date' column to datetime
            try:
                df['Date'] = pd.to_datetime(df['Date'])
            except Exception as date_error:
                st.error(f"⚠️ Error parsing 'Date' column: {date_error}")
                st.stop()

            # Sort the data chronologically
            df = df.sort_values('Date')

            # Remove any missing values
            df = df.dropna(subset=['Date', 'CargoVolume'])

            # Set Date as index for time-series plotting
            df.set_index('Date', inplace=True)

            # Ensure CargoVolume is numeric
            try:
                df['CargoVolume'] = pd.to_numeric(df['CargoVolume'])
            except Exception as conv_error:
                st.error(f"⚠️ Error converting 'CargoVolume' to numeric: {conv_error}")
                st.stop()

            # ----------------------------
            # Line Chart Visualization
            # ----------------------------
            st.subheader("📈 Historical Cargo Volume Trend")
            st.line_chart(df['CargoVolume'])

            # ----------------------------
            # Basic Stats Summary
            # ----------------------------
            st.subheader("📌 Summary Statistics")
            st.write(df['CargoVolume'].describe())

            # ----------------------------
            # Optional: Filter by Year or Range
            # ----------------------------
            st.subheader("🔍 Optional: Filter by Date Range")
            min_date = df.index.min()
            max_date = df.index.max()

            start_date, end_date = st.date_input(
                "Select date range:",
                value=[min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )

            if start_date and end_date:
                filtered_df = df.loc[start_date:end_date]

                st.markdown(f"### 📅 Filtered Data from {start_date} to {end_date}")
                st.dataframe(filtered_df, use_container_width=True)

                st.subheader("📉 Filtered Cargo Volume Trend")
                st.line_chart(filtered_df['CargoVolume'])

    except Exception as e:
        st.error(f"🚨 An unexpected error occurred while processing your file: {e}")

else:
    st.info("👈 Please upload a CSV file to get started.")
