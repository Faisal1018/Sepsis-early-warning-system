import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="ICU Clinical Intelligence Platform",
    page_icon="🩺",
    layout="wide"
)

# =====================================================
# CLEAN MEDICAL CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background-color:#f8fafc;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#ffffff;
    border-right:1px solid #e2e8f0;
}

/* Card Style */
.card{
    background:#ffffff;
    border:1px solid #e2e8f0;
    border-radius:15px;
    padding:20px;
    box-shadow:0 2px 6px rgba(0,0,0,0.05);
}

/* Title */
.big-title{
    font-size:36px;
    font-weight:700;
    color:#0f172a;
}

.sub{
    color:#475569;
    font-size:16px;
}

/* Driver */
.driver-card{
    background:#ffffff;
    border-left:5px solid #ef4444;
    padding:10px;
    border-radius:8px;
    margin-bottom:8px;
    color:#0f172a;
}

/* Footer */
.author-card{
    background:#ffffff;
    border:1px solid #e2e8f0;
    padding:20px;
    border-radius:15px;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# MODEL
# =====================================================

model = joblib.load("models/xgboost_sepsis_model.pkl")

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="card">

<div class="big-title">
🩺 ICU Clinical Intelligence Platform
</div>

<div class="sub">
AI Powered Early Sepsis Detection & Clinical Decision Support System
</div>

</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================================
# SIDEBAR INPUT
# =====================================================

st.sidebar.title("🏥 Patient Assessment")

age = st.sidebar.slider("Age",18,90,65)
gender = st.sidebar.selectbox("Gender",["Female","Male"])
gender_value = 1 if gender=="Male" else 0

hr = st.sidebar.slider("Heart Rate",40,220,90)
o2sat = st.sidebar.slider("Oxygen Saturation",50,100,97)
temp = st.sidebar.slider("Temperature",30.0,42.0,37.0)
sbp = st.sidebar.slider("SBP",60,220,120)
map_val = st.sidebar.slider("MAP",40,150,80)
resp = st.sidebar.slider("Respiratory Rate",5,50,18)
creatinine = st.sidebar.slider("Creatinine",0.1,10.0,1.0)
wbc = st.sidebar.slider("WBC",1.0,50.0,11.0)
glucose = st.sidebar.slider("Glucose",50,400,120)
hosp_adm = st.sidebar.slider("HospAdmTime",-200,0,-10)
iculos = st.sidebar.slider("ICULOS",1,300,30)

# =====================================================
# DATAFRAME
# =====================================================

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

# =====================================================
# PREDICTION
# =====================================================

prob = model.predict_proba(patient)[0][1]
risk = round(prob*100,2)

if risk < 30:
    status = "LOW RISK 🟢"
elif risk < 60:
    status = "MODERATE RISK 🟡"
else:
    status = "HIGH RISK 🔴"

# =====================================================
# KPI
# =====================================================

k1,k2,k3,k4 = st.columns(4)

k1.metric("❤️ Heart Rate", hr)
k2.metric("🫁 Resp Rate", resp)
k3.metric("🌡 Temp", temp)
k4.metric("🏥 ICU Hours", iculos)

st.write("")

# =====================================================
# MAIN
# =====================================================

left,center,right = st.columns([1,2,1])

with left:
    st.markdown("### 👤 Patient Info")
    st.metric("Age",age)
    st.metric("Gender",gender)
    st.metric("WBC",wbc)
    st.metric("Creatinine",creatinine)

with center:

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={"text":"Sepsis Risk Score"},
        number={"suffix":"%"},
        gauge={
            "axis":{"range":[0,100]},
            "bar":{"color":"#ef4444"},
            "steps":[
                {"range":[0,30],"color":"#22c55e"},
                {"range":[30,60],"color":"#f59e0b"},
                {"range":[60,100],"color":"#ef4444"}
            ]
        }
    ))

    fig.update_layout(
        height=420,
        paper_bgcolor="#ffffff",
        font={"color":"#0f172a"}
    )

    st.plotly_chart(fig,use_container_width=True)

with right:
    st.markdown("### 🚨 Status")
    st.metric("Risk",f"{risk}%")
    st.info(status)
    st.metric("Model","XGBoost")

# =====================================================
# TREND
# =====================================================

st.markdown("---")

col1,col2 = st.columns(2)

with col1:

    trend = pd.DataFrame({
        "Hour":[1,2,3,4,5,6],
        "Risk":[25,35,41,57,63,risk]
    })

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=trend["Hour"],
        y=trend["Risk"],
        mode="lines+markers"
    ))

    fig2.update_layout(
        title="Risk Trend",
        height=350
    )

    st.plotly_chart(fig2,use_container_width=True)

with col2:

    st.markdown("### 🧠 AI Risk Drivers")

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
        drivers.append("⬆ Long ICU Stay")
    if wbc > 12:
        drivers.append("⬆ Abnormal WBC Count")

    if len(drivers)==0:
        drivers.append("✅ No major risk driver detected")

    for d in drivers:
        st.markdown(f"<div class='driver-card'>{d}</div>", unsafe_allow_html=True)

# =====================================================
# RECOMMENDATION
# =====================================================

st.markdown("---")

st.subheader("👨‍⚕️ Clinical Recommendation")

if risk >= 70:
    st.error("High Risk: Immediate physician review required.")
elif risk >= 40:
    st.warning("Moderate Risk: Monitor closely.")
else:
    st.success("Low Risk: Routine monitoring.")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
<div class='author-card'>

<h3>👨‍💻 Developed By</h3>

<b>MD. FAISAL HAMID</b><br><br>

Machine Learning Engineer<br>
Healthcare AI | Explainable AI | XGBoost<br><br>

🩺 ICU Sepsis Early Warning System

</div>
""", unsafe_allow_html=True)
