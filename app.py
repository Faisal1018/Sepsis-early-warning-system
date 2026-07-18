import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="ICU Clinical Intelligence Platform",
    page_icon="🩺",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp{
    background-color:#020617;
}

.main-title{
    font-size:42px;
    font-weight:700;
    color:white;
}

.subtitle{
    color:#cbd5e1;
    font-size:18px;
}

.card{
    background:#0f172a;
    padding:20px;
    border-radius:20px;
    border:1px solid #1e293b;
}

.driver-card{
    background:#111827;
    padding:12px;
    border-left:5px solid #ef4444;
    border-radius:10px;
    margin-bottom:8px;
    color:white;
}

.high{
    color:#ef4444;
    font-size:36px;
    font-weight:bold;
}

.medium{
    color:#f59e0b;
    font-size:36px;
    font-weight:bold;
}

.low{
    color:#22c55e;
    font-size:36px;
    font-weight:bold;
}

.metric-box{
    background:#0f172a;
    border-radius:15px;
    padding:15px;
    border:1px solid #1e293b;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD MODEL
# ==================================================

model = joblib.load(
    "models/xgboost_sepsis_model.pkl"
)

# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div style="
background:linear-gradient(90deg,#0f172a,#1e3a8a);
padding:30px;
border-radius:20px;
border:1px solid #334155;
">

<h1 style="color:white;">
🩺 ICU Clinical Intelligence Platform
</h1>

<p style="color:#cbd5e1;font-size:18px;">
AI-Powered Early Sepsis Risk Prediction &
Clinical Decision Support System
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🧾 Patient Information")

age = st.sidebar.slider("Age",18,90,65)

gender = st.sidebar.selectbox(
    "Gender",
    ["Female","Male"]
)

gender_value = 1 if gender=="Male" else 0

hr = st.sidebar.slider(
    "Heart Rate",
    40,220,90)

o2sat = st.sidebar.slider(
    "Oxygen Saturation",
    50,100,97)

temp = st.sidebar.slider(
    "Temperature",
    30.0,42.0,37.0)

sbp = st.sidebar.slider(
    "SBP",
    60,220,120)

map_val = st.sidebar.slider(
    "MAP",
    40,150,80)

resp = st.sidebar.slider(
    "Respiratory Rate",
    5,50,18)

creatinine = st.sidebar.slider(
    "Creatinine",
    0.1,10.0,1.0)

wbc = st.sidebar.slider(
    "WBC",
    1.0,50.0,11.0)

glucose = st.sidebar.slider(
    "Glucose",
    50,400,120)

hosp_adm = st.sidebar.slider(
    "Hospital Admission Time",
    -200,0,-10)

iculos = st.sidebar.slider(
    "ICU Length Of Stay",
    1,300,30)

# ==================================================
# INPUT DATA
# ==================================================

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
    "Gender":[gender_value],
    "HospAdmTime":[hosp_adm],
    "ICULOS":[iculos]

})

# ==================================================
# PREDICTION
# ==================================================

prob = model.predict_proba(patient)[0][1]

risk = round(prob*100,2)

# ==================================================
# STATUS
# ==================================================

if risk < 30:
    status = "LOW RISK"
    status_color = "low"

elif risk < 60:
    status = "MODERATE RISK"
    status_color = "medium"

else:
    status = "HIGH RISK"
    status_color = "high"

# ==================================================
# KPI CARDS
# ==================================================

st.write("")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric("❤️ Heart Rate",f"{hr} bpm")

with c2:
    st.metric("🫁 Resp Rate",f"{resp}/min")

with c3:
    st.metric("🌡 Temp",f"{temp}°C")

with c4:
    st.metric("🏥 ICU Hours",iculos)

# ==================================================
# MAIN LAYOUT
# ==================================================

left,center,right = st.columns([1,2,1])

# ===============================

with left:

    st.markdown("### 👤 Patient Summary")

    st.metric("Age", age)
    st.metric("Gender", gender)
    st.metric("WBC", wbc)
    st.metric("Creatinine", creatinine)

# ===============================

with center:

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=risk,

        number={
            "suffix":"%"
        },

        title={
            "text":"Sepsis Risk Score"
        },

        gauge={

            "axis":{"range":[0,100]},

            "bar":{"color":"#ef4444"},

            "steps":[

                {"range":[0,30],"color":"#10b981"},

                {"range":[30,60],"color":"#f59e0b"},

                {"range":[60,100],"color":"#ef4444"}

            ]

        }

    ))

    fig.update_layout(
        height=450,
        paper_bgcolor="#020617",
        font={"color":"white"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ===============================

with right:

    st.markdown("### 🚨 Clinical Status")

    st.markdown(
        f"<p class='{status_color}'>{status}</p>",
        unsafe_allow_html=True
    )

    st.metric(
        "Predicted Risk",
        f"{risk}%"
    )

    st.metric(
        "Model",
        "XGBoost"
    )

# ==================================================
# AI RISK DRIVERS
# ==================================================

st.markdown("---")

st.markdown("## 🧠 AI Risk Drivers")

drivers = []

if hr > 100:
    drivers.append("⬆ Elevated Heart Rate")

if resp > 22:
    drivers.append("⬆ Elevated Respiratory Rate")

if temp > 38:
    drivers.append("⬆ Fever Detected")

if creatinine > 1.5:
    drivers.append("⬆ Kidney Dysfunction")

if iculos > 48:
    drivers.append("⬆ Prolonged ICU Stay")

if wbc > 12:
    drivers.append("⬆ Abnormal White Blood Cell Count")

if len(drivers) == 0:
    drivers.append("✅ No major risk drivers detected")

for d in drivers:
    st.markdown(
        f"""
        <div class='driver-card'>
        {d}
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# RECOMMENDATIONS
# ==================================================

st.markdown("---")

st.markdown("## 👨‍⚕️ Clinical Recommendation")

if risk >= 70:

    st.error("""

    High probability of sepsis detected.

    Recommended Actions:

    • Immediate physician review

    • Continuous monitoring

    • Infection screening

    • Laboratory investigation

    • Early intervention consideration

    """)

elif risk >= 40:

    st.warning("""

    Moderate sepsis risk detected.

    Recommended Actions:

    • Increased observation

    • Repeat vital assessment

    • Monitor laboratory trends

    """)

else:

    st.success("""

    Low sepsis risk profile.

    Continue routine ICU monitoring.

    """)

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.markdown("""
<div style="
background:#0f172a;
padding:20px;
border-radius:20px;
border:1px solid #1e293b;
">

<h3 style="color:white;">
👨‍💻 Developed By
</h3>

<p style="color:#cbd5e1;">

<b>MD. FAISAL HAMID</b>

<br><br>

AI • Machine Learning • Healthcare Analytics

<br><br>

🏆 Explainable ICU Sepsis Early Warning System

<br>

XGBoost + SHAP + Streamlit

</p>

</div>
""", unsafe_allow_html=True)
