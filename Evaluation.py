import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from modules.Eval import hasil_eval, visual_eval, koefisien_regresi

# =============================
# CONFIG HALAMAN
# =============================
st.set_page_config(
    page_title="Evaluation - Linear Regression",
    layout="wide"
)

st.title("📊 Model Evaluation – Linear Regression")
st.markdown("Evaluasi performa model regresi linear menggunakan metrik error dan visualisasi.")

# =============================
# DATA SIMULASI (GANTI DENGAN DATA ASLI)
# =============================
X = np.arange(1, 101).reshape(-1, 1)
y = np.arange(1, 101)

feature_names = ["PC4"]   # karena 1 fitur PCA

# =============================
# TRAIN MODEL ASLI
# =============================
model = LinearRegression()
model.fit(X, y)

X_test = X
y_test = y

# =============================
# PANGGIL BACKEND EVALUATION
# =============================
eval_result = hasil_eval(model, X_test, y_test)

# =============================
# SECTION 1: METRIC CARDS
# =============================
st.subheader("📌 Evaluation Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("MAE", f"{eval_result['MAE']:.2f}")
col2.metric("MSE", f"{eval_result['MSE']:.2f}")
col3.metric("RMSE", f"{eval_result['RMSE']:.2f}")
col4.metric("R² Score", f"{eval_result['R2']:.2f}")

# =============================
# SECTION 2: VISUALISASI
# =============================
st.subheader("📈 Visualization")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("**Actual vs Predicted**")
    fig1 = visual_eval(y_test, eval_result["y_pred"])
    st.pyplot(fig1)

with col_right:
    st.markdown("**Residual Plot**")
    residuals = y_test - eval_result["y_pred"]

    fig2, ax2 = plt.subplots()
    ax2.scatter(eval_result["y_pred"], residuals)
    ax2.axhline(0)
    ax2.set_xlabel("Predicted Value")
    ax2.set_ylabel("Residual")
    ax2.set_title("Residual Distribution")

    st.pyplot(fig2)

# =============================
# SECTION 3: KOEFISIEN REGRESI
# =============================
st.subheader("📐 Koefisien Regresi")

coef_df, intercept = koefisien_regresi(model, feature_names)

st.dataframe(coef_df, use_container_width=True)
st.markdown(f"**Intercept:** {intercept:.4f}")

# =============================
# SECTION 4: INTERPRETASI
# =============================
st.subheader("🧠 Interpretation")

st.markdown("""
- **MAE & RMSE kecil** → prediksi mendekati nilai aktual  
- **R² mendekati 1** → model menjelaskan variasi data dengan baik  
- **Residual acak di sekitar nol** → asumsi regresi linear terpenuhi  

""")
