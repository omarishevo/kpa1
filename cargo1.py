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
y = location_grouped['C]()_
