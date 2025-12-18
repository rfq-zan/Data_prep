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

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(page_title="Agricultural Production Analysis", layout="wide")
st.title("📊 Agricultural Production Analysis ")

# ------------------------
# LOAD DATA
# ------------------------
df = load_data()

# ------------------------
# Remove Unnecessary Columns (Country, Year, Country Code)
# ------------------------
df_cleaned = df.drop(columns=['Country', 'Year', 'Country Code'], errors='ignore')

# ------------------------
# DATA OVERVIEW
# ------------------------
st.subheader("1️⃣ Data Overview")
st.write("Here's a preview of the raw data:")
st.dataframe(df_cleaned)

# ------------------------
# Line Plot for Data Overview (Before Further Processing)
# ------------------------
st.subheader("2️⃣ Line Plot Overview")
st.write("Visualizing trends for numeric columns (grid view).")

numeric_cols_for_lineplot = df_cleaned.select_dtypes(include=['float64', 'int64']).columns.tolist()

num_cols = 3
cols = st.columns(num_cols)
for idx, col in enumerate(numeric_cols_for_lineplot):
    with cols[idx % num_cols]:
        st.pyplot(lineplot(df_cleaned, col, f"Line Plot of {col}"))

# ------------------------
# Data Cleaning
# ------------------------
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

missing_per_col_after = df_cleaned.isnull().sum().sort_values(ascending=False)
missing_per_col_after = missing_per_col_after[missing_per_col_after > 0]

st.write("Missing values per column (after):")
if len(missing_per_col_after) > 0:
    st.dataframe(missing_per_col_after.rename("Missing Count"))
else:
    st.success("All missing values handled (no missing values remain).")

# ------------------------
# Remove Duplicates (More visual)
# ------------------------
st.subheader("4️⃣ Duplicate Value Removal")

dup_count_before = int(df_cleaned.duplicated().sum())
total_before = int(df_cleaned.shape[0])

c1, c2, c3 = st.columns(3)
c1.metric("Rows (Before)", total_before)
c2.metric("Duplicates Found", dup_count_before)
c3.metric("Duplicate Rate", f"{(dup_count_before/total_before*100):.2f}%" if total_before else "0.00%")

progress_bar = st.progress(0)
with st.spinner("Removing duplicates..."):
    df_cleaned = df_cleaned.drop_duplicates()
    progress_bar.progress(100)

total_after = int(df_cleaned.shape[0])
st.success("Duplicate rows removed successfully.")
st.metric("Rows (After)", total_after)

# ------------------------
# Outlier Checking (BEFORE log, using Boxplot only)
# ------------------------
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

# ------------------------
# Log Transformation (AS IN .ipynb: np.log1p applied AFTER outlier checking)
# ------------------------
st.subheader("6️⃣ Log Transformation (np.log1p) — After Outlier Checking")
st.write("Applying `np.log1p()` directly to the selected columns (no ln* columns are created).")

log_columns = ['Production', 'Land', 'Labor', 'N', 'P', 'K', 'Pesticides', 'fert']
log_columns = [c for c in log_columns if c in df_cleaned.columns]

df_log = df_cleaned.copy()
df_log[log_columns] = np.log1p(df_log[log_columns])

st.write("Preview of log-transformed columns:")
st.dataframe(df_log[log_columns].head())

# Optional: show boxplot AFTER log (to prove outlier shrinkage visually)
st.subheader("7️⃣ Outlier Checking (After Log)")
grid2 = st.columns(2)
for idx, col in enumerate(selected_cols):
    if col in df_log.columns:
        with grid2[idx % 2]:
            st.pyplot(boxplot(df_log, col, f"Boxplot of {col} (After Log)"))

# ------------------------
# PCA (FIXED to match your .ipynb logic: full PCA + explained variance table)
# ------------------------
st.subheader("8️⃣ PCA (Principal Component Analysis) — Based on Log Data")
st.write("PCA fitted on `data_log.drop(columns=['Production','Country','Year'])` style (robust drop).")

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

st.write("PCA Explained Variance Table:")
st.dataframe(pca_variance)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(1, len(explained_var) + 1), explained_var, marker='o', label='Explained Variance')
ax.plot(range(1, len(explained_var) + 1), cum_var, marker='x', label='Cumulative Variance')
ax.set_xlabel("Principal Component")
ax.set_ylabel("Variance")
ax.set_title("PCA Variance (Explained & Cumulative)")
ax.legend()
st.pyplot(fig)

# ------------------------
# Correlation Heatmap (Before vs After Log)
# ------------------------
st.subheader("9️⃣ Correlation Heatmap (Before vs After Log)")

st.write("Correlation BEFORE log (numeric only):")
num_before = df_cleaned.select_dtypes(include='number')
corr_before = num_before.corr()

fig1, ax1 = plt.subplots(figsize=(12, 7))
sns.heatmap(corr_before, annot=True, fmt=".2f")
ax1.set_title("Correlation Heatmap — Before Log")
st.pyplot(fig1)

st.write("Correlation AFTER log (numeric only):")
num_after = df_log.select_dtypes(include='number')
corr_after = num_after.corr()

fig2, ax2 = plt.subplots(figsize=(12, 7))
sns.heatmap(corr_after, annot=True, fmt=".2f")
ax2.set_title("Correlation Heatmap — After Log")
st.pyplot(fig2)

# ------------------------
# Visualizations (After Outlier Handling) -> boxplot only (as per your revision)
# ------------------------
st.subheader("🔟 Final Boxplot (After Log)")
column_to_plot = st.selectbox(
    "Select a column for boxplot (after log):",
    df_log.select_dtypes(include="number").columns.tolist()
)
st.pyplot(boxplot(df_log, column_to_plot, f"Boxplot of {column_to_plot} (After Log)"))

# ------------------------
# EDA
# ------------------------
st.subheader("1️⃣1️⃣ EDA: Summary Statistics (After Log)")
st.dataframe(summary_statistics(df_log))

# ------------------------
# Export / Download
# ------------------------
st.subheader("📥 Download / Export")
download_csv(df_log)

stats_clean = summary_statistics(df_log)
export_data_pdf(df_log, stats_clean, filename="report_agriculture.pdf")

fig_example = histogram(df_log, column_to_plot, f"Histogram of {column_to_plot}")
export_fig_to_pdf(fig_example, filename=f"{column_to_plot}_histogram.pdf")
