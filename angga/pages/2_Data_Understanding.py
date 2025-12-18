import streamlit as st
from pathlib import Path
import pandas as pd

# =====================================================
# PATH & ASSETS
# =====================================================
BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"

# =====================================================
# SIDEBAR (KONSISTEN DENGAN BUSINESS UNDERSTANDING)
# =====================================================
with st.sidebar:
    st.markdown("## 🌾 CRISP-DM Framework")
    st.markdown("---")
    st.markdown("### Tahapan Analisis")
    st.markdown("""
    - Business Understanding  
    - **Data Understanding**  
    - Data Preparation  
    - Modeling  
    - Evaluation  
    """)
    st.markdown("---")
    st.caption("Proyek Akademik Data Science\nSkala Riset")

# =====================================================
# HEADER
# =====================================================
st.markdown("""
# 📊 Data Understanding  
### Analisis Produksi Pertanian di Kawasan Asia
""")

st.markdown("""
Tahap **Data Understanding** bertujuan untuk memahami karakteristik data
secara empiris dan statistik, termasuk struktur variabel, distribusi data,
kualitas data, serta potensi permasalahan awal yang dapat memengaruhi
tahapan analisis selanjutnya.
""")

st.divider()

# =====================================================
# PLACEHOLDER KONTEN
# =====================================================
st.subheader("1. Struktur dan Tipe Data")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("2. Statistik Deskriptif")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("3. Distribusi dan Pola Data")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("4. Identifikasi Outlier Awal")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.subheader("5. Analisis Korelasi Awal")
st.markdown("_Bagian ini akan diisi oleh peneliti._")

st.divider()
st.caption("Data Understanding | Proyek Data Science Akademik")
