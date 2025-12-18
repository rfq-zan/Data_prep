import streamlit as st
from pathlib import Path

# =====================================================
# PATH
# =====================================================
BASE_DIR = Path(__file__).resolve().parents[1]

# =====================================================
# SIDEBAR (KONSISTEN)
# =====================================================
with st.sidebar:
    st.markdown("## 🌾 CRISP-DM Framework")
    st.markdown("---")
    st.markdown("### Tahapan Analisis")
    st.markdown("""
    - Business Understanding  
    - Data Understanding  
    - **Data Preparation**  
    - Modeling  
    - Evaluation  
    """)
    st.markdown("---")
    st.caption("Proyek Akademik Data Science\nSkala Riset")

# =====================================================
# HEADER
# =====================================================
st.markdown("""
# 🧹 Data Preparation  
### Analisis Produksi Pertanian di Kawasan Asia
""")

st.markdown("""
Tahap **Data Preparation** berfokus pada proses pembersihan,
transformasi, dan penyiapan data agar siap digunakan
dalam pemodelan statistik dan machine learning.
""")

st.divider()

# =====================================================
# PLACEHOLDER KONTEN
# =====================================================
st.subheader("1. Penanganan Missing Value")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("2. Transformasi Data")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("3. Penanganan Outlier")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("4. Seleksi dan Reduksi Fitur")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("5. Dataset Final untuk Modeling")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.divider()
st.caption("Data Preparation | Proyek Data Science Akademik")
