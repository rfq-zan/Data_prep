import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

from modules.data_loader import load_data
from modules.preprocessing import summary_statistics, handle_missing_values
from modules.visualization import histogram, boxplot, lineplot
from modules.export_utils import download_csv, export_data_pdf, export_fig_to_pdf

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Agricultural Production Analysis",
    layout="wide"
)

# =========================
# CSS — BLUE OUTLINE CONTAINER (VS CODE DARK)
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: 'Segoe UI', sans-serif;
}

/* Container styling */
section[data-testid="stContainer"] {
    background-color: #161b22;
    border: 2px solid #58a6ff;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 28px;
    box-shadow: 0 0 12px rgba(88,166,255,0.25);
}

/* Headings */
h1, h2, h3 {
    color: #58a6ff;
    font-weight: 700;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: #0d1117;
    border-radius: 10px;
}

/* Metric */
[data-testid="metric-container"] {
    background-color: #0d1117;
    border: 1px solid #30363d;
    padding: 16px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("📊 Agricultural Production Analysis")
st.caption("Modern EDA Dashboard • VS Code Dark High Contrast Theme")

# =========================
# LOAD DATA
# =========================
df = load_data()
df_cleaned = df.drop(columns=['Country', 'Year', 'Country Code'], errors='ignore')

# =========================
# 1️⃣ DATA OVERVIEW
# =========================
with st.container(border=True):
    st.subheader("1️⃣ Data Overview")
    st.write("Here's a preview of the raw data:")
    st.dataframe(df_cleaned, use_container_width=True)

# =========================
# 2️⃣ LINE PLOT OVERVIEW
# =========================
with st.container(border=True):
    st.subheader("2️⃣ Line Plot Overview")
    st.write("Visualizing trends for numeric columns (grid view).")

    numeric_cols_for_lineplot = df_cleaned.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cols = st.columns(3)

    for idx, col in enumerate(numeric_cols_for_lineplot):
        with cols[idx % 3]:
            st.pyplot(lineplot(df_cleaned, col, f"Line Plot of {col}"))

# =========================
# 3️⃣ DATA CLEANING
# =========================
with st.container(border=True):
    st.subheader("3️⃣ Data Cleaning")
    st.write("Handling missing values by filling them with the median of each numeric column.")

    missing_per_col = df_cleaned.isnull().sum().sort_values(ascending=False)
    missing_per_col = missing_per_col[missing_per_col > 0]

    st.write("Missing values per column (before):")
    if len(missing_per_col) > 0:
        st.dataframe(missing_per_col.rename("Missing Count"))
    else:
        st.info("No missing values found.")

    df_cleaned = handle_missing_values(df_cleaned, strategy='median')

    missing_per_col_after = df_cleaned.isnull().sum()
    missing_per_col_after = missing_per_col_after[missing_per_col_after > 0]

    st.write("Missing values per column (after):")
    if len(missing_per_col_after) > 0:
        st.dataframe(missing_per_col_after.rename("Missing Count"))
    else:
        st.success("All missing values handled (no missing values remain).")

# =========================
# 4️⃣ DUPLICATE REMOVAL
# =========================
with st.container(border=True):
    st.subheader("4️⃣ Duplicate Value Removal")

    dup_count_before = int(df_cleaned.duplicated().sum())
    total_before = int(df_cleaned.shape[0])

    c1, c2, c3 = st.columns(3)
    c1.metric("Rows (Before)", total_before)
    c2.metric("Duplicates Found", dup_count_before)
    c3.metric("Duplicate Rate", f"{(dup_count_before/total_before*100):.2f}%")

    progress_bar = st.progress(0)
    with st.spinner("Removing duplicates..."):
        df_cleaned = df_cleaned.drop_duplicates()
        progress_bar.progress(100)

    st.success("Duplicate rows removed successfully.")
    st.metric("Rows (After)", int(df_cleaned.shape[0]))

# =========================
# 5️⃣ OUTLIER CHECK (BEFORE LOG)
# =========================
with st.container(border=True):
    st.subheader("5️⃣ Outlier Checking (Before Log)")
    st.write("Boxplot is used to visually check outliers BEFORE log transformation.")

    selected_cols = st.multiselect(
        "Select columns for outlier checking:",
        df_cleaned.select_dtypes(include="number").columns.tolist(),
        default=df_cleaned.select_dtypes(include="number").columns.tolist()
    )

    grid = st.columns(2)
    for idx, col in enumerate(selected_cols):
        with grid[idx % 2]:
            st.pyplot(boxplot(df_cleaned, col, f"Boxplot of {col} (Before Log)"))

# =========================
# 6️⃣ LOG TRANSFORMATION
# =========================
with st.container(border=True):
    st.subheader("6️⃣ Log Transformation (np.log1p) — After Outlier Checking")

    log_columns = ['Production', 'Land', 'Labor', 'N', 'P', 'K', 'Pesticides', 'fert']
    log_columns = [c for c in log_columns if c in df_cleaned.columns]

    df_log = df_cleaned.copy()
    df_log[log_columns] = np.log1p(df_log[log_columns])

    st.write("Preview of log-transformed columns:")
    st.dataframe(df_log[log_columns].head())

# =========================
# 7️⃣ OUTLIER CHECK (AFTER LOG)
# =========================
with st.container(border=True):
    st.subheader("7️⃣ Outlier Checking (After Log)")
    grid2 = st.columns(2)

    for idx, col in enumerate(selected_cols):
        if col in df_log.columns:
            with grid2[idx % 2]:
                st.pyplot(boxplot(df_log, col, f"Boxplot of {col} (After Log)"))

# =========================
# 8️⃣ PCA
# =========================
with st.container(border=True):
    st.subheader("8️⃣ PCA (Principal Component Analysis) — Based on Log Data")

    X_pca = df_log.drop(columns=['Production', 'Country', 'Year'], errors='ignore')
    X_pca = X_pca.select_dtypes(include='number').dropna()

    pca = PCA()
    pca.fit(X_pca)

    explained_var = pca.explained_variance_ratio_
    cum_var = np.cumsum(explained_var)

    pca_variance = pd.DataFrame({
        'PC': [f'PC{i+1}' for i in range(len(explained_var))],
        'Explained Variance': explained_var,
        'Cumulative Variance': cum_var
    })

    st.dataframe(pca_variance)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(range(1, len(explained_var) + 1), explained_var, marker='o', label='Explained')
    ax.plot(range(1, len(explained_var) + 1), cum_var, marker='x', label='Cumulative')
    ax.legend()
    st.pyplot(fig)

# =========================
# 9️⃣ CORRELATION HEATMAP
# =========================
with st.container(border=True):
    st.subheader("9️⃣ Correlation Heatmap (Before vs After Log)")

    fig1, ax1 = plt.subplots(figsize=(12, 7))
    sns.heatmap(df_cleaned.select_dtypes(include='number').corr(), annot=True, fmt=".2f")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(12, 7))
    sns.heatmap(df_log.select_dtypes(include='number').corr(), annot=True, fmt=".2f")
    st.pyplot(fig2)

# =========================
# 🔟 FINAL BOXPLOT
# =========================
with st.container(border=True):
    st.subheader("🔟 Final Boxplot (After Log)")
    column_to_plot = st.selectbox(
        "Select a column:",
        df_log.select_dtypes(include="number").columns.tolist()
    )
    st.pyplot(boxplot(df_log, column_to_plot, f"Boxplot of {column_to_plot} (After Log)"))

# =========================
# 1️⃣1️⃣ EDA
# =========================
with st.container(border=True):
    st.subheader("1️⃣1️⃣ EDA: Summary Statistics (After Log)")
    st.dataframe(summary_statistics(df_log))

# =========================
# 📥 EXPORT
# =========================
with st.container(border=True):
    st.subheader("📥 Download / Export")

    download_csv(df_log)

    stats_clean = summary_statistics(df_log)
    export_data_pdf(df_log, stats_clean, filename="report_agriculture.pdf")

    fig_example = histogram(df_log, column_to_plot, f"Histogram of {column_to_plot}")
    export_fig_to_pdf(fig_example, filename=f"{column_to_plot}_histogram.pdf")
