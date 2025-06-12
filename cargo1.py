import streamlit as st
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("C:\Users\Administrator\Desktop\class work\kpa_personnel_dataset_final.csv")

# Encode experience level bins
df['Experience Level'] = pd.cut(
    df['Years of Experience'],
    bins=[0, 5, 10, 20, 50],
    labels=['Novice (0–5)', 'Junior (5–10)', 'Mid (10–20)', 'Senior (20+)']
)

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Shift filter
shift_options = ['All'] + sorted(df['Shift'].dropna().unique().tolist())
selected_shift = st.sidebar.selectbox("Shift", shift_options)

# Work location filter
location_options = ['All'] + sorted(df['Work Location'].dropna().unique().tolist())
selected_location = st.sidebar.selectbox("Work Location", location_options)

# Experience level filter
experience_options = ['All'] + df['Experience Level'].dropna().unique().astype(str).tolist()
selected_experience = st.sidebar.selectbox("Experience Level", experience_options)

# Apply filters
filtered_df = df.copy()

if selected_shift != 'All':
    filtered_df = filtered_df[filtered_df['Shift'] == selected_shift]

if selected_location != 'All':
    filtered_df = filtered_df[filtered_df['Work Location'] == selected_location]

if selected_experience != 'All':
    filtered_df = filtered_df[filtered_df['Experience Level'].astype(str) == selected_experience]

# Main UI
st.title("📦 KPA Personnel Explorer")
st.markdown("Interactively filter the Kenya Ports Authority personnel dataset.")

st.success(f"Displaying {len(filtered_df)} records after filtering.")

st.dataframe(
    filtered_df[['ID Number', 'Name', 'Shift', 'Work Location', 'Years of Experience', 'Experience Level']],
    use_container_width=True
)
