🩺 Explainable ICU Sepsis Early Warning System

An end-to-end Healthcare AI system that predicts Sepsis Risk in ICU Patients using clinical data, machine learning, and explainable AI techniques.

This project leverages patient vital signs, laboratory measurements, and ICU stay information to provide early sepsis risk assessment, enabling proactive clinical intervention.

🚀 Live Demo

🔗 Streamlit App:

Plain Text
Coming Soon

Show more lines
📂 GitHub Repository
Plain Text
https://github.com/Faisal1018/Explainable-ICU-Sepsis-Early-Warning-System

Show more lines
🎯 Problem Statement

Sepsis is a life-threatening medical condition caused by the body's extreme response to infection.

Early identification is critical because delayed diagnosis can significantly increase mortality risk.

This project aims to develop an AI-powered Clinical Decision Support System that:

✅ Detects high-risk ICU patients

✅ Provides risk probability

✅ Explains predictions using Explainable AI (SHAP)

✅ Assists clinicians in early intervention

📊 Dataset Information
Dataset

PhysioNet 2019 Sepsis Challenge Dataset

Summary
Plain Text
Total Records : 546,122



Total Patients : 14,057



Observation Type : Hourly ICU Measurements



Target Variable : SepsisLabel



Positive Patients : 1,239



Negative Patients : 12,818

Show more lines
Clinical Features
Plain Text
Heart Rate (HR)



Respiratory Rate (Resp)



Oxygen Saturation (O2Sat)



Temperature



Blood Pressure



Creatinine



White Blood Cell Count



Glucose



Age



ICU Length Of Stay (ICULOS)



Hospital Admission Time

Show more lines
🔬 Exploratory Data Analysis

Key findings from EDA:

Sepsis Patients Showed

✅ Higher Heart Rate

✅ Higher Respiratory Rate

✅ Higher WBC Count

✅ Higher Creatinine Levels

✅ Longer ICU Stay

These findings align with known clinical indicators of sepsis and organ dysfunction.

⚙️ Machine Learning Pipeline
Plain Text
Data Understanding

 ↓

Clinical EDA

 ↓

Missing Value Analysis

 ↓

Feature Selection

 ↓

Patient-Level Train/Test Split

 ↓

Data Leakage Prevention

 ↓

Missing Value Imputation

 ↓

Model Development

 ↓

Explainable AI

 ↓

Deployment

Show more lines
🛡️ Data Leakage Prevention

Most healthcare projects fail due to patient leakage.

Instead of using a random row-level split:

❌ Random Train/Test Split

This project uses:

✅ Patient-Level Train/Test Split

Ensuring:

Plain Text
No patient appears in both

training and testing sets.

Show more lines
🤖 Models Evaluated
1. Logistic Regression

Used as baseline model.

Initial Observation
Plain Text
Accuracy ≈ 98%

Show more lines

However:

Plain Text
Recall = 0



Show more lines

The model failed to identify sepsis patients due to severe class imbalance.

2. Balanced Logistic Regression
Plain Text
Recall Improved



Recall ≈ 64%

Show more lines

but generated excessive false alarms.

3. Random Forest
Plain Text
ROC-AUC = 0.796

Show more lines

Strong benchmark tree-based model.

🏆 Final Model: XGBoost
Performance
Plain Text
ROC-AUC = 0.806

Show more lines
Why XGBoost?

✅ Handles class imbalance effectively

✅ Captures non-linear clinical relationships

✅ Supports feature interaction learning

✅ Compatible with Explainable AI (SHAP)

✅ Best overall performance

📈 Threshold Optimization

Default Threshold:

Plain Text
0.50

Show more lines
Results
Plain Text
Precision = 0.14



Recall = 0.36

Show more lines

Optimized Threshold:

Plain Text
0.30

Show more lines
Results
Plain Text
Precision = 0.11



Recall = 0.50

Show more lines
Key Insight

Changing the decision threshold significantly improved clinical sensitivity without retraining the model.

🔍 Explainable AI (SHAP)

To improve clinical trust and transparency, SHAP was used to interpret model predictions.

Top Risk Drivers
Plain Text
ICULOS



HospAdmTime



Respiratory Rate



Heart Rate



Age



Temperature



SBP

Show more lines
Clinical Interpretation

Higher:

Plain Text
Respiratory Rate



Heart Rate



Age



ICU Stay Duration

Show more lines

generally increase predicted sepsis risk.

📊 Model Comparison
Model	ROC-AUCLogistic Regression	Baseline
Random Forest	0.796
XGBoost	0.806

🏆 Best Model: XGBoost

🖥️ Dashboard Features

Premium Clinical Decision Support Dashboard built with Streamlit.

Features

✅ Real-Time Prediction

✅ Risk Probability Gauge

✅ Clinical Risk Categories

✅ ICU Monitoring Interface

✅ AI-Powered Clinical Interpretation

✅ High-Risk Patient Identification

📸 Project Screenshots
Dataset Overview

Add screenshot

Missing Value Analysis

Add screenshot

Correlation Heatmap

Add screenshot

XGBoost Confusion Matrix

Add screenshot

Feature Importance

Add screenshot

SHAP Summary Plot

Add screenshot

Streamlit Dashboard

Add screenshot

Risk Prediction Example

Add screenshot

🛠️ Tech Stack
Programming
Plain Text
Python

Show more lines
Data Analysis
Plain Text
Pandas

NumPy

Show more lines
Visualization
Plain Text
Matplotlib



Seaborn



Plotly

Show more lines
Machine Learning
Plain Text
Scikit-Learn



XGBoost

Show more lines
Explainable AI
Plain Text
SHAP

Show more lines
Deployment
Plain Text
Streamlit

Show more lines
Version Control
Plain Text
Git

GitHub

Show more lines
📂 Project Structure
Plain Text
Explainable-ICU-Sepsis-Early-Warning-System/



│

├── app/

│ └── streamlit_app.py

│

├── data/

│ ├── raw/

│ └── processed/

│

├── models/

│ └── xgboost_sepsis_model.pkl

│

├── notebooks/

│ ├── 01_data_audit.ipynb

│ ├── 02_eda.ipynb

│ ├── 03_data_cleaning.ipynb

│ ├── 04_baseline_model.ipynb

│ └── 05_xgboost_model.ipynb

│

├── reports/

│

├── requirements.txt

│

└── README.md

Show more lines
⚙️ Run Locally
Shell
git clone <repository-url>



cd Explainable-ICU-Sepsis-Early-Warning-System



pip install -r requirements.txt



streamlit run app/streamlit_app.py

Show more lines
👨‍💻 Author

MD. FAISAL HAMID

🔗 GitHub:
 https://github.com/Faisal1018

🔗 LinkedIn:
 (Add LinkedIn URL)