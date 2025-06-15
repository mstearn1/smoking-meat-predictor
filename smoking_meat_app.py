import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_excel("SmokingMeatWithScores.xlsx")

df = load_data()

# Constants for estimates
meat_temps = {
    "Brisket": 203, "Pork Shoulder": 195, "Baby Back Ribs": 190, "Spare Ribs": 190,
    "Whole Chicken": 165, "Turkey Breast": 160, "Lamb Shoulder": 190, "Beef Short Ribs": 200
}
hours_per_lb = {
    "Brisket": 1.5, "Pork Shoulder": 1.2, "Baby Back Ribs": 1.0, "Spare Ribs": 1.2,
    "Whole Chicken": 0.75, "Turkey Breast": 0.75, "Lamb Shoulder": 1.3, "Beef Short Ribs": 1.4
}

# UI Inputs
st.title("Weber Smokey Mountain Smoking Predictor")

col1, col2 = st.columns(2)

with col1:
    meat_type = st.selectbox("Select Meat Type", list(meat_temps.keys()))
    weight = st.slider("Meat Weight (lbs)", 3.0, 16.0, 8.0)
    smoker_temp = st.selectbox("Smoker Temperature (°F)", [225, 250, 275])
    weather = st.selectbox("Weather Condition", ["Sunny", "Cloudy", "Rainy", "Windy", "Humid", "Dry"])

with col2:
    outside_temp = st.slider("Outside Temp (°F)", 40, 100, 70)
    zip_code = st.text_input("ZIP Code", "90210")
    date = st.date_input("Smoking Date", datetime.date.today())
    start_time = st.time_input("Start Time", datetime.time(6, 0))

# Estimations
est_cook_time = round(weight * hours_per_lb[meat_type], 2)
target_internal_temp = meat_temps[meat_type]

# Score prediction logic
def predict_score(weather, smoker_temp, est_cook_time):
    base_score = 9.0
    if weather in ["Rainy", "Windy"]:
        base_score += 0.3
    if smoker_temp == 275:
        base_score -= 0.2
    return max(min(round(base_score + np.random.normal(0, 0.3), 1), 10), 1)

predicted_score = predict_score(weather, smoker_temp, est_cook_time)

# Output
st.subheader("Predicted Smoking Results")
st.write(f"**Target Internal Temp**: {target_internal_temp}°F")
st.write(f"**Estimated Cook Time**: {est_cook_time} hours")
st.write(f"**Predicted Review Score**: {predicted_score} / 10")

st.subheader("Compare to Historical Data")
st.dataframe(df[df["Meat Type"] == meat_type][[
    "Date", "Meat Weight (lbs)", "Smoker Temp (°F)", "Final Internal Temp (°F)",
    "Estimated Cook Time (hrs)", "Actual Cook Time (hrs)",
    "Franklin Expert Score", "Third-Party Review Score"
]])
