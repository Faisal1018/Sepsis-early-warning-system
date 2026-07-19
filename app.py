import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ICU Sepsis Early Warning System",
    page_icon="🩺",
    layout="wide"
)

# --------------------------------------------------
# MODERN CSS (UPGRADED UI)
# --------------------------------------------------

st.markdown("""
<style>

body {
    background-color: #0f172a;
    color: white;
}

.block-container {
    padding-top: 1rem;
}

/* Card */
.card {
    background: #111827;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1f2937;
}

/* Risk Text */
.high-risk {
    color:#ef4444;
    font-size:30px;
    font-weight:bold;
}

.medium-risk {
    color:#f59e0b;
    font-size:30px;
    font-weight:bold;
}

.low-risk {
    color:#22c55e;
    font-size:30px;
    font-weight:bold;
}

/* Title */
.title {
    font-size:38px;
    font-weight:bold;
}

/* Author */
.author {
    color: gray;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = joblib.load("models/xgboost_sepsis_model.pkl")

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("<div class='title'>🩺 ICU Sepsis Early Warning System</div>", unsafe_allow_html=True)
st.markdown("<div class='author'>Author: Faisal1018</div>", unsafe_allow_html=True)

st.markdown("""
AI-powered clinical decision support platform for early sepsis risk assessment in ICU patients.
""")

st.write("---")

# --------------------------------------------------
# SIDEBAR (UNCHANGED)
# --------------------------------------------------

st.sidebar.header("Patient Clinical Information")

age = st.sidebar.slider("Age",18,90,65)
gender = st.sidebar.selectbox("Gender",[0,1])
hr = st.sidebar.slider("Heart Rate",40,220,90)
o2sat = st.sidebar.slider("Oxygen Saturation",50,100,97)
temp = st.sidebar.slider("Temperature",30.0,42.0,37.0)
sbp = st.sidebar.slider("SBP",60,220,120)
map_val = st.sidebar.slider("MAP",40,150,80)
resp = st.sidebar.slider("Respiratory Rate",5,50,18)
creatinine = st.sidebar.slider("Creatinine",0.1,10.0,1.0)
wbc = st.sidebar.slider("WBC",1.0,50.0,11.0)
glucose = st.sidebar.slider("Glucose",50,400,120)
hosp_adm = st.sidebar.slider("Hosp Admission Time",-200,0,-10)
iculos = st.sidebar.slider("ICU Length Of Stay",1,300,30)

# --------------------------------------------------
# DATAFRAME (UNCHANGED)
# --------------------------------------------------

patient = pd.DataFrame({
    "HR":[hr],
    "O2Sat":[o2sat],
    "Temp":[temp],
    "SBP":[sbp],
    "MAP":[map_val],
    "Resp":[resp],
    "Creatinine":[creatinine],
    "WBC":[wbc],
    "Glucose":[glucose],
    "Age":[age],
    "Gender":[gender],
    "HospAdmTime":[hosp_adm],
    "ICULOS":[iculos]
})

# --------------------------------------------------
# PREDICTION (UNCHANGED)
# --------------------------------------------------

prob = model.predict_proba(patient)[0][1]
risk = prob * 100

# --------------------------------------------------
# STATUS (UNCHANGED)
# --------------------------------------------------

if risk < 30:
    status = "LOW RISK"
    status_class = "low-risk"
elif risk < 60:
    status = "MODERATE RISK"
    status_class = "medium-risk"
else:
    status = "HIGH RISK"
    status_class = "high-risk"

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

col1, col2, col3 = st.columns([1,2,1])

# LEFT CARD
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Patient Summary")
    st.metric("Age", age)
    st.metric("Heart Rate", hr)
    st.metric("Resp", resp)
    st.metric("Temperature", temp)
    st.markdown("</div>", unsafe_allow_html=True)

# CENTER GAUGE
with col2:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={'text':"Sepsis Risk (%)"},
        gauge={
            'axis': {'range':[0,100]},
            'bar': {'color':"#ef4444"},
            'steps':[
                {'range':[0,30],'color':'#22c55e'},
                {'range':[30,60],'color':'#f59e0b'},
                {'range':[60,100],'color':'#ef4444'}
            ]
        }
    ))

    fig.update_layout(height=420)

    st.plotly_chart(fig, use_container_width=True)

# RIGHT CARD
with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Clinical Status")
    st.markdown(f"<p class='{status_class}'>{status}</p>", unsafe_allow_html=True)
    st.metric("Risk %", round(risk,2))
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# AI EXPLANATION (UNCHANGED)
# --------------------------------------------------

st.markdown("---")
st.subheader("AI Clinical Interpretation")

drivers = []

if resp > 22:
    drivers.append("↑ Elevated Respiratory Rate")

if hr > 100:
    drivers.append("↑ Tachycardia (High Heart Rate)")

if temp > 38:
    drivers.append("↑ Fever")

if iculos > 48:
    drivers.append("↑ Long ICU Stay")

if creatinine > 1.5:
    drivers.append("↑ Kidney Dysfunction (Creatinine)")

if len(drivers) == 0:
    drivers.append("No major risk drivers detected")

for d in drivers:
    st.write("•", d)

st.markdown("---")

st.success("""
Model: XGBoost  
ROC-AUC: 0.806  
Dataset: PhysioNet Sepsis Challenge Dataset
""")
