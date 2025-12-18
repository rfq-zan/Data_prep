import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Agricultural Production Analysis",
    layout="wide"
)

# -------------------------
# TITLE
# -------------------------
st.title("Agricultural Production Analysis")
st.subheader("Data Understanding")

st.divider()

# -------------------------
# LOAD DATA
# -------------------------
CSV_URL = "https://docs.google.com/spreadsheets/d/14N_7TYa72pCxbJE5m3W9RwoZVGKqOP4r/export?format=csv&gid=970731575"
data = pd.read_csv(CSV_URL)

# =========================
# 1. DATA OVERVIEW
# =========================
st.header("1. Data Overview")

st.write("Preview of the dataset:")
st.dataframe(data.head(), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Rows", data.shape[0])
with col2:
    st.metric("Total Columns", data.shape[1])

st.divider()

# =========================
# 2. DATA STRUCTURE
# =========================
st.header("2. Data Structure")

info_df = pd.DataFrame({
    "Column": data.columns,
    "Data Type": data.dtypes.astype(str),
    "Non-Null Count": data.notnull().sum().values
})

st.dataframe(info_df, use_container_width=True)

st.divider()

# =========================
# 3. MISSING VALUES
# =========================
st.header("3. Missing Values")

missing_df = pd.DataFrame({
    "Column": data.columns,
    "Missing Values": data.isnull().sum().values,
    "Percentage (%)": (data.isnull().sum() / len(data) * 100).round(2).values
})

st.dataframe(missing_df, use_container_width=True)

st.divider()

# =========================
# 4. DUPLICATE DATA
# =========================
st.header("4. Duplicate Check")

duplicate_count = data.duplicated().sum()
st.write(f"Total duplicate rows: **{duplicate_count}**")

st.divider()

# =========================
# 5. DESCRIPTIVE STATISTICS
# =========================
st.header("5. Descriptive Statistics")

st.dataframe(data.describe(), use_container_width=True)

st.divider()

# =========================
# 6. OUTLIER DETECTION
# =========================
st.header("6. Outlier Detection (Boxplot)")

exclude_cols = ["Country_Code", "Year"]

numeric_cols = [
    col for col in data.select_dtypes(include=np.number).columns
    if col not in exclude_cols
]
selected_col = st.selectbox("Select numeric column:", numeric_cols)

fig, ax = plt.subplots(figsize=(6, 2))
sns.boxplot(x=data[selected_col], ax=ax)
ax.set_title(f"Boxplot of {selected_col}")

st.pyplot(fig)

st.divider()

# =========================
# 7. TREND / LINE PLOT
# =========================
st.header("7. Trend Analysis")

trend_col = st.selectbox(
    "Select column for trend visualization:",
    numeric_cols
)
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(data[trend_col])
ax.set_title(f"Trend of {trend_col}")
ax.set_xlabel("Index")
ax.set_ylabel(trend_col)

st.pyplot(fig)


st.divider()

# -------------------------
# FOOTER
# -------------------------
st.caption("Data Understanding Phase — CRISP-DM")
