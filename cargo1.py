import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Page configuration
st.set_page_config(page_title="KPA Cargo Volume Flow Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("kpa_personnel_dataset_final.csv")
    return df

df = load_data()

st.title("📊 KPA Cargo Volume Flow Forecast Dashboard")

# --- Preprocessing ---
# Encode shift types
shift_mapping = {'Day': 1, 'Night': 2, 'Rotational': 3}
df['Shift_encoded'] = df['Shift'].map(shift_mapping)

# Group data by work location
location_grouped = df.groupby('Work Location').agg({
    'Years of Experience': 'mean',
    'Shift_encoded': 'mean',
    'ID Number': 'count'
}).rename(columns={
    'Years of Experience': 'Avg_Experience',
    'Shift_encoded': 'Avg_Shift',
    'ID Number': 'Personnel_Count'
})

# Add synthetic cargo volume flow based on a formula
np.random.seed(42)
location_grouped['Cargo_Volume_Flow'] = (
    location_grouped['Avg_Experience'] * 2 +
    location_grouped['Avg_Shift'] * 5 +
    location_grouped['Personnel_Count'] * 3 +
    np.random.normal(0, 5, size=location_grouped.shape[0])
)

# --- Modeling ---
X = location_grouped[['Avg_Experience', 'Avg_Shift', 'Personnel_Count']]
y = location_grouped['Cargo_Volume_Flow']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Fit Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

# --- Streamlit Dashboard Layout ---
tab1, tab2, tab3 = st.tabs(["📈 Summary", "📊 Visualizations", "🔍 Feature Insights"])

# --- Tab 1: Summary ---
with tab1:
    st.subheader("🔢 Model Summary Metrics")
    st.metric(label="Root Mean Squared Error (RMSE)", value=f"{rmse:.2f}")
    st.metric(label="R² Score", value=f"{r2:.2f}")

    st.subheader("🧾 Aggregated Data by Work Location")
    st.dataframe(location_grouped.reset_index())

# --- Tab 2: Visualizations ---
with tab2:
    st.subheader("📍 Cargo Volume Flow by Work Location")
    st.bar_chart(location_grouped['Cargo_Volume_Flow'])

    st.subheader("📌 Correlation Matrix")
    corr_df = location_grouped.corr().round(2)
    st.dataframe(corr_df)

# --- Tab 3: Feature Insights ---
with tab3:
    st.subheader("🔧
