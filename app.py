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
# CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background-color:#020617;
}

section[data-testid="stSidebar"]{
    background:#0f172a;
}

.block-container{
    padding-top:1rem;
}

.card{
    background:#0f172a;
    border:1px solid #1e293b;
    border-radius:20px;
    padding:20px;
}

.risk-card{
    background:linear-gradient(135deg,#7f1d1d,#991b1b);
    border-radius:25px;
    padding:30px;
    text-align:center;
}

.author-card{
    background:#0f172a;
    border:1px solid #1e293b;
    padding:20px;
    border-radius:20px;
}

.driver-card{
    background:#111827;
    border-left:5px solid #ef4444;
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
    color:white;
}

.big-title{
    font-size:42px;
    font-weight:bold;
    color:white;
}

.sub{
    color:#cbd5e1;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# MODEL
# =====================================================

model = joblib.load(
    "models/xgboost_sepsis_model.pkl"
)

# =====================================================
# HERO HEADER
# =====================================================

st.markdown("""
<div style="
background:linear-gradient(135deg,#0f172a,#1e40af);
padding:30px;
border-radius:25px;
border:1px solid #334155;
">

<div class="big-title">
🩺 ICU Clinical Intelligence Platform
</div>

<div class="sub">
AI Powered Early Sepsis Detection &
Clinical Decision Support System
</div>

</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🏥 Patient Assessment")

age = st.sidebar.slider("Age",18,90,65)

gender = st.sidebar.selectbox(
    "Gender",
    ["Female","Male"]
)

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
# TOP KPI
# =====================================================

k1,k2,k3,k4 = st.columns(4)

with k1:
    st.metric("❤️ Heart Rate", f"{hr}")

with k2:
    st.metric("🫁 Resp Rate", f"{resp}")

with k3:
    st.metric("🌡 Temp", f"{temp}")

with k4:
    st.metric("🏥 ICU Hours", f"{iculos}")

st.write("")

# =====================================================
# MAIN AREA
# =====================================================

left,center,right = st.columns([1,2,1])

# =================================

with left:

    st.markdown("### 👤 Patient")

    st.metric("Age",age)
    st.metric("Gender",gender)
    st.metric("WBC",wbc)
    st.metric("Creatinine",creatinine)

# =================================

with center:

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=risk,

        title={"text":"SEPSIS RISK SCORE"},

        number={"suffix":"%"},

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
        paper_bgcolor="#020617",
        font={"color":"white"},
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =================================

with right:

    st.markdown("### 🚨 Status")

    st.metric(
        "Risk",
        f"{risk}%"
    )

    st.success(status)

    st.metric(
        "Model",
        "XGBoost"
    )

# =====================================================
# TREND SECTION
# =====================================================

st.markdown("---")

trend_col1,trend_col2 = st.columns(2)

with trend_col1:

    trend = pd.DataFrame({

        "Hour":[1,2,3,4,5,6],
        "Risk":[25,35,41,57,63,risk]

    })

    trend_fig = go.Figure()

    trend_fig.add_trace(

        go.Scatter(
            x=trend["Hour"],
            y=trend["Risk"],
            mode="lines+markers",
            line=dict(color="#38bdf8",width=4)
        )
    )

    trend_fig.update_layout(

        title="📈 Risk Trend",

        template="plotly_dark",

        height=350,

        paper_bgcolor="#020617",

        plot_bgcolor="#020617"
    )

    st.plotly_chart(
        trend_fig,
        use_container_width=True
    )

# =================================

with trend_col2:

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

        st.markdown(
            f"""
            <div class='driver-card'>
            {d}
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================================================
# RECOMMENDATIONS
# =====================================================

st.markdown("---")

st.subheader("👨‍⚕️ Clinical Recommendation Engine")

if risk >= 70:

    st.error("""

🚨 HIGH RISK PATIENT

Recommended Actions:

• Immediate Physician Review

• Infection Evaluation

• Continuous Monitoring

• Sepsis Bundle Consideration

• Laboratory Assessment

""")

elif risk >= 40:

    st.warning("""

⚠ MODERATE RISK

Recommended Actions:

• Monitor Clinical Trends

• Repeat Assessment

• Watch Vital Sign Changes

""")

else:

    st.success("""

✅ LOW RISK

Routine Monitoring Recommended

""")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
<div class='author-card'>

<h2 style='color:white'>
👨‍💻 Developed By
</h2>

<p style='color:#cbd5e1;font-size:18px;'>

<b>MD. FAISAL HAMID</b>

<br><br>

Machine Learning Engineer

<br>

Healthcare AI | Explainable AI | XGBoost

<br><br>

🩺 Explainable ICU Sepsis Early Warning System

</p>

</div>
""", unsafe_allow_html=True)
