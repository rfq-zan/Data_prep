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
# DATA OVERVIEW
# ------------------------
st.subheader("1️⃣ Data Overview")
st.write("Here's a preview of the raw data:")
st.dataframe(df.head())

# ------------------------
# Data Cleaning
# ------------------------
st.subheader("2️⃣ Data Cleaning")
st.write("Handling missing values by filling them with the median of each column.")

# Display missing values before cleaning
missing_cols = df.columns[df.isnull().any()]
st.write("Columns with missing values:", missing_cols)

# Handle Missing Values (median strategy)
df_cleaned = handle_missing_values(df, strategy='median')

# Show missing values after cleaning
missing_cols_after = df_cleaned.columns[df_cleaned.isnull().any()]
st.write("Columns with missing values after handling:", missing_cols_after)

# ------------------------
# Remove Duplicates
# ------------------------
st.write("Removing duplicate rows from the data.")
df_cleaned = df_cleaned.drop_duplicates()
st.write(f"Number of rows after removing duplicates: {df_cleaned.shape[0]}")

# ------------------------
# Log Transformation (As per .ipynb)
# ------------------------
st.subheader("3️⃣ Log Transformation")
st.write("Applying log transformation to skewed columns.")

# Apply log transformation to selected columns (if they exist in the dataset)
log_columns = ['Production', 'Land', 'Labor', 'N', 'P', 'K', 'Pesticides', 'fert']
for col in log_columns:
    if col in df_cleaned.columns:
        df_cleaned[f'ln{col}'] = np.log(df_cleaned[col] + 1)  # Add 1 to avoid log(0)

# Show the transformed data
st.write("Here's a preview of the log-transformed columns:")
st.dataframe(df_cleaned[[f'ln{col}' for col in log_columns]].head())

# ------------------------
# Outlier Checking with Boxplot and Lineplot (Before Removal)
# ------------------------
st.subheader("4️⃣ Outlier Checking (Before Removal)")

selected_cols = st.multiselect("Select columns for outlier checking:", df.select_dtypes(include="number").columns.tolist(), default=df.select_dtypes(include="number").columns.tolist())

# Create grid for plots
cols = st.columns(2)  # Create two columns for a grid layout

# Boxplot for outlier detection
for idx, col in enumerate(selected_cols):
    with cols[idx % 2]:  # Alternate between columns
        st.pyplot(boxplot(df_cleaned, col, f"Boxplot of {col} (Before Outlier Removal)"))

# Lineplot to visualize trends
for idx, col in enumerate(selected_cols):
    with cols[(idx + len(selected_cols)) % 2]:  # Alternate between columns
        st.pyplot(lineplot(df_cleaned, col, f"Line Plot of {col}"))

# ------------------------
# Outlier Detection using PCA (No IQR)
# ------------------------
st.subheader("5️⃣ Outlier Detection using PCA")
st.write("Removing outliers using PCA and visualizing the results.")

# Standardize the data before applying PCA
numeric_cols = df_cleaned.select_dtypes(include=['float64', 'int64']).columns.tolist()
df_cleaned_pca = df_cleaned[numeric_cols].dropna()

# Standardize the data
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_cleaned_pca)

# Apply PCA to reduce dimensionality
pca = PCA(n_components=2)  # Reduce to 2 components for visualization
df_pca = pca.fit_transform(df_scaled)

# Visualize the PCA output
st.write("PCA Components:")
st.write(pd.DataFrame(df_pca, columns=['PC1', 'PC2']).head())

# Create a plot of the PCA components
df_pca_df = pd.DataFrame(df_pca, columns=['PC1', 'PC2'])

# Identify outliers based on PCA
# We'll use the distance from the mean (a simple method for identifying outliers in PCA space)
mean_pc1 = np.mean(df_pca_df['PC1'])
mean_pc2 = np.mean(df_pca_df['PC2'])

# Calculate the Euclidean distance from the mean for each point
df_pca_df['Distance'] = np.sqrt((df_pca_df['PC1'] - mean_pc1)**2 + (df_pca_df['PC2'] - mean_pc2)**2)

# Outliers are points with distance > 95th percentile
threshold = np.percentile(df_pca_df['Distance'], 95)
df_pca_df['Outlier'] = df_pca_df['Distance'] > threshold

# Plot PCA with outliers highlighted
plt.figure(figsize=(10, 6))
sns.scatterplot(x='PC1', y='PC2', data=df_pca_df, hue='Outlier', palette='coolwarm', s=100)
plt.title("PCA of Data with Outliers Highlighted")
plt.tight_layout()
st.pyplot(plt)

# ------------------------
# Correlation Heatmap
# ------------------------
st.subheader("6️⃣ Correlation Heatmap")
st.write("Visualizing the correlation between features using a heatmap.")

# Select only numeric columns for correlation calculation
numeric_cols = df_cleaned.select_dtypes(include=['float64', 'int64']).columns.tolist()

# Calculate correlation matrix for numeric columns only
correlation_matrix = df_cleaned[numeric_cols].corr()

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
st.pyplot(plt)

# ------------------------
# Visualizations (After Outlier Handling)
# ------------------------
st.subheader("7️⃣ Visualizing the Cleaned and Transformed Data (After Outlier Handling)")
column_to_plot = st.selectbox("Select a column for histogram:", df_cleaned.select_dtypes(include="number").columns.tolist())
st.pyplot(histogram(df_cleaned, column_to_plot, f"Histogram of {column_to_plot} (After Transformation)"))

# ------------------------
# Exploratory Data Analysis (EDA)
# ------------------------
st.subheader("8️⃣ EDA: Summary Statistics")
st.write("Here's a summary of the data after cleaning and transformations:")
st.dataframe(summary_statistics(df_cleaned))

# ------------------------
# Export / Download
# ------------------------
st.subheader("📥 Download / Export")

download_csv(df_cleaned)

stats_clean = summary_statistics(df_cleaned)
export_data_pdf(df_cleaned, stats_clean, filename="report_agriculture.pdf")

fig_example = histogram(df_cleaned, column_to_plot, f"Histogram of {column_to_plot}")
export_fig_to_pdf(fig_example, filename=f"{column_to_plot}_histogram.pdf")
