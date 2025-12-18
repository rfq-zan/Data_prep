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
    - Data Preparation  
    - Modeling  
    - **Evaluation**  
    """)
    st.markdown("---")
    st.caption("Proyek Akademik Data Science\nSkala Riset")

# =====================================================
# HEADER
# =====================================================
st.markdown("""
# 📈 Evaluation  
### Analisis Produksi Pertanian di Kawasan Asia
""")

st.markdown("""
Tahap **Evaluation** bertujuan untuk mengevaluasi kinerja model,
membandingkan seluruh skenario yang diuji,
serta menentukan pendekatan terbaik
berdasarkan kriteria statistik dan interpretasi ekonomi.
""")

st.divider()

# =====================================================
# PLACEHOLDER KONTEN
# =====================================================
st.subheader("1. Metode Evaluasi Model")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("2. Perbandingan Antar Skenario")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("3. Pemilihan Model Terbaik")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("4. Implikasi Ekonomi dan Kebijakan")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.divider()
st.caption("Evaluation | Proyek Data Science Akademik")
