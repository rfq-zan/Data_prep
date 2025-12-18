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
    - **Modeling**  
    - Evaluation  
    """)
    st.markdown("---")
    st.caption("Proyek Akademik Data Science\nSkala Riset")

# =====================================================
# HEADER
# =====================================================
st.markdown("""
# 🤖 Modeling  
### Analisis Produksi Pertanian di Kawasan Asia
""")

st.markdown("""
Tahap **Modeling** mencakup pembangunan dan pengujian model statistik
berdasarkan skenario yang telah dirancang, dengan fokus pada
hubungan antara input produksi dan output pertanian.
""")

st.divider()

# =====================================================
# PLACEHOLDER KONTEN
# =====================================================
st.subheader("1. Spesifikasi Model")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("2. Implementasi Skenario Modeling")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("3. Estimasi Model Regresi")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("4. Interpretasi Koefisien")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.divider()
st.caption("Modeling | Proyek Data Science Akademik")
