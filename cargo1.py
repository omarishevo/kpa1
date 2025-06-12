import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(page_title="KPA Cargo Volume Flow Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("kpa_personnel_dataset_final.csv")
    return df

df = load_data()
st.title("📊 KPA Cargo Volume Flow Forecast Dashboard")

# --- Preprocessing ---
shift_mapping = {'Day': 1, 'Night': 2, 'Rotational': 3}
df['Shift_encoded'] = df['Shift'].map(shift_mapping)

location_grouped = df.groupby('Work Location').agg({
    'Years of Experience': 'mean',
    'Shift_encoded': 'mean',
    'ID Number': 'count'
}).rename(columns={
    'Years of Experience': 'Avg_Experience',
    'Shift_encoded': 'Avg_Shift',
    'ID Number': 'Personnel_Count'
})

# Synthetic Cargo Volume Flow
np.random.seed(42)
location_grouped['Cargo_Volume_Flow'] = (
    location_grouped['Avg_Experience'] * 2 +
    location_grouped['Avg_Shift'] * 5 +
    location_grouped['Personnel_Count'] * 3 +
    np.random.normal(0, 5, size=location_grouped.shape[0])
)

# --- Model ---
X = location_grouped[['Avg_Experience', 'Avg_Shift', 'Personnel_Count']]
y = location_grouped['Cargo_Volume_Flow']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y
