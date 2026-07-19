import streamlit as st

# Page config
st.set_page_config(page_title="ICU Clinical Intelligence", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0b1220;
    color: #e5e7eb;
}

.main {
    background-color: #0b1220;
}

.card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0,0,0,0.4);
}

.metric {
    font-size: 36px;
    font-weight: 600;
    color: #ffffff;
}

.label {
    color: #9ca3af;
    font-size: 14px;
}

.header {
    font-size: 28px;
    font-weight: 600;
    color: #22c55e;
}

.subtext {
    color: #94a3b8;
}

.sidebar .stSlider > div {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("🩺 Patient Assessment")

age = st.sidebar.slider("Age", 0, 100, 65)
gender = st.sidebar.selectbox("Gender", ["Female", "Male"])
oxygen = st.sidebar.slider("Oxygen Saturation", 0, 100, 95)

# ------------------ HEADER ------------------
st.markdown("""
<div class="card">
    <div class="header">🩺 ICU Clinical Intelligence Platform</div>
    <div class="subtext">AI Powered Early Sepsis Detection & Clinical Decision Support</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------ METRICS ------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <div class="label">Heart Rate</div>
        <div class="metric">90</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="label">Resp Rate</div>
        <div class="metric">18</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="label">Temperature</div>
        <div class="metric">37.0</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <div class="label">ICU Hours</div>
        <div class="metric">30</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------ RISK STATUS ------------------
st.markdown("""
<div style="
    background: linear-gradient(90deg, #16a34a, #15803d);
    padding: 20px;
    border-radius: 12px;
    color: white;
    font-size: 18px;
    font-weight: 500;
    text-align:center;
">
    ✅ Low Risk: Routine Monitoring
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown("""
<div class="card" style="text-align:center;">
    <div class="subtext">Developed by</div>
    <div style="font-size:20px;">MD. FAISAL HAMID</div>
    <div class="subtext">Machine Learning Engineer</div>
    <div class="subtext">Healthcare AI | Explainable AI | XGBoost</div>
</div>
""", unsafe_allow_html=True)
