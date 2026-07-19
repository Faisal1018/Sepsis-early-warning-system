import streamlit as st
import numpy as np
import joblib

# ---------------- LOAD MODEL ----------------
model = joblib.load("model.pkl")  # <-- tomar model file

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="ICU Clinical Dashboard", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>

body {
    background-color: #0b1220;
    color: #e5e7eb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Card */
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 14px;
    backdrop-filter: blur(8px);
    box-shadow: 0 0 15px rgba(0,0,0,0.3);
}

/* Title */
.title {
    font-size: 28px;
    font-weight: 700;
    color: #22c55e;
}

.subtitle {
    color: #9ca3af;
}

/* Metrics */
.metric {
    font-size: 34px;
    font-weight: 600;
    color: #ffffff;
}

.label {
    font-size: 13px;
    color: #9ca3af;
}

/* Risk */
.low {
    background: linear-gradient(90deg,#16a34a,#15803d);
}

.medium {
    background: linear-gradient(90deg,#f59e0b,#d97706);
}

.high {
    background: linear-gradient(90deg,#ef4444,#dc2626);
}

.riskbox {
    padding: 20px;
    border-radius: 12px;
    text-align:center;
    color:white;
    font-size:18px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🩺 Patient Assessment")

age = st.sidebar.slider("Age", 0, 100, 65)
gender = st.sidebar.selectbox("Gender", ["Female", "Male"])
oxygen = st.sidebar.slider("Oxygen Saturation", 0, 100, 95)
heart_rate = st.sidebar.slider("Heart Rate", 30, 180, 90)
resp_rate = st.sidebar.slider("Resp Rate", 5, 40, 18)
temperature = st.sidebar.slider("Temperature", 30.0, 42.0, 37.0)
icu_hours = st.sidebar.slider("ICU Hours", 0, 200, 30)

# ---------------- INPUT PREP ----------------
# IMPORTANT: same order as training
gender_val = 1 if gender == "Male" else 0

input_data = np.array([[age, gender_val, oxygen, heart_rate, resp_rate, temperature, icu_hours]])

# ---------------- MODEL PREDICTION ----------------
prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0][1]

# ---------------- RISK LOGIC ----------------
if probability < 0.3:
    risk_text = f"🟢 Low Risk ({probability*100:.2f}%)"
    risk_class = "low"
elif probability < 0.7:
    risk_text = f"🟡 Medium Risk ({probability*100:.2f}%)"
    risk_class = "medium"
else:
    risk_text = f"🔴 High Risk ({probability*100:.2f}%)"
    risk_class = "high"

# ---------------- HEADER ----------------
st.markdown("""
<div class="card">
    <div class="title">🩺 ICU Clinical Intelligence Platform</div>
    <div class="subtitle">AI Powered Early Sepsis Detection & Clinical Decision Support</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- METRICS ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="label">Heart Rate</div>
        <div class="metric">{heart_rate}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="label">Resp Rate</div>
        <div class="metric">{resp_rate}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="label">Temperature</div>
        <div class="metric">{temperature}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="card">
        <div class="label">ICU Hours</div>
        <div class="metric">{icu_hours}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- PATIENT INFO ----------------
colA, colB, colC = st.columns(3)

with colA:
    st.markdown(f"""
    <div class="card">
        <div class="label">Age</div>
        <div class="metric">{age}</div>
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown(f"""
    <div class="card">
        <div class="label">Gender</div>
        <div class="metric">{gender}</div>
    </div>
    """, unsafe_allow_html=True)

with colC:
    st.markdown(f"""
    <div class="card">
        <div class="label">Oxygen Saturation</div>
        <div class="metric">{oxygen}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- RISK DISPLAY ----------------
st.markdown(f"""
<div class="riskbox {risk_class}">
    {risk_text}
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- PROBABILITY BAR ----------------
st.subheader("Sepsis Probability")
st.progress(int(probability * 100))
st.write(f"{probability*100:.2f}%")

# ---------------- DEBUG (optional remove later) ----------------
# st.write("Prediction:", prediction)
# st.write("Probability:", probability)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="card" style="text-align:center;">
    <div class="subtitle">Developed By</div>
    <div style="font-size:20px;">MD. FAISAL HAMID</div>
    <div class="subtitle">Machine Learning Engineer</div>
    <div class="subtitle">Healthcare AI | Explainable AI | XGBoost</div>
    <br>
    <div class="subtitle">ICU Sepsis Early Warning System</div>
</div>
""", unsafe_allow_html=True)
