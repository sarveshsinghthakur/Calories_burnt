import streamlit as st
import requests

st.set_page_config(page_title="Calories Burnt Predictor", page_icon="🔥")

st.title("🔥 Calories Burnt Predictor")

st.markdown("Enter your details to predict calories burned:")

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    gender_val = "1" if gender == "Male" else "0"
    age = st.number_input("Age", min_value=1, max_value=100, value=25)
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
    weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=70.0)

with col2:
    duration = st.number_input("Duration (minutes)", min_value=1.0, max_value=300.0, value=30.0)
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=40.0, max_value=220.0, value=120.0)
    body_temp = st.number_input("Body Temperature (°C)", min_value=35.0, max_value=42.0, value=37.0)

if st.button("Predict Calories", type="primary"):
    payload = {
        "gender": gender_val,
        "age": age,
        "height": height,
        "weight": weight,
        "duration": duration,
        "heart_rate": heart_rate,
        "body_temp": body_temp
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Calories Burnt: {result['prediction']:.2f}")
        else:
            st.error(f"Error: {response.text}")
    except Exception as e:
        st.error(f"Could not connect to backend. Make sure FastAPI server is running. Error: {e}")