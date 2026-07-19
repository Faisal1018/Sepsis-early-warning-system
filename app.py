import streamlit as st
import numpy as np
import pickle

# -----------------------------
# Load Model
# -----------------------------
model = pickle.load(open("models/xgboost_sepsis_model.pkl", "rb"))

st.set_page_config(page_title="Sepsis Early Warning System", layout="wide")

st.title("🩺 Sepsis Early Warning Dashboard")

# -----------------------------
# Sidebar Input
# -----------------------------
st.sidebar.header("Patient Input Data")

def user_input():
    HR = st.sidebar.number_input("Heart Rate", 30, 200, 80)
    O2Sat = st.sidebar.number_input("Oxygen Saturation", 50, 100, 95)
    Temp = st.sidebar.number_input("Temperature", 30.0, 42.0, 37.0)
    SBP = st.sidebar.number_input("Systolic BP", 50, 200, 110)
    MAP = st.sidebar.number_input("MAP", 40, 150, 80)
    Resp = st.sidebar.number_input("Respiration Rate", 5, 60, 20)

    data = np.array([[HR, O2Sat, Temp, SBP, MAP, Resp]])
    return data

input_data = user_input()

# -----------------------------
# Prediction
# -----------------------------
if st.button("🔍 Predict"):

    try:
        # Probability বের করা (VERY IMPORTANT)
        prob = model.predict_proba(input_data)[0][1]
        prediction = model.predict(input_data)[0]

        st.subheader("📊 Prediction Result")

        # -----------------------------
        # Risk Logic (REAL MODEL BASED)
        # -----------------------------
        if prob < 0.3:
            risk = "LOW"
            color = "green"
        elif prob < 0.7:
            risk = "MEDIUM"
            color = "orange"
        else:
            risk = "HIGH"
            color = "red"

        # -----------------------------
        # Dashboard Output
        # -----------------------------
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Sepsis Probability", f"{prob*100:.2f}%")

        with col2:
            st.markdown(
                f"<h2 style='color:{color};'>Risk Level: {risk}</h2>",
                unsafe_allow_html=True
            )

        # -----------------------------
        # Progress Bar (Dynamic Meter)
        # -----------------------------
        st.progress(int(prob * 100))

    except Exception as e:
        st.error(f"❌ Error: {e}")
