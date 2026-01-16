import streamlit as st
import pandas as pd
import plotly.express as px
from modules.quality_analyzer import analyze_quality
from modules.ui_components import render_sidebar_progress, display_lottie_spinner

# 1. Sidebar Progress
render_sidebar_progress("Quality")

st.header("🧪 Data Quality Analysis")

# --------------------------------------------------
# Guard: Ensure data is uploaded
# --------------------------------------------------
if st.session_state.raw_df is None:
    st.warning("⚠️ No dataset found. Please upload a CSV file first.")
    st.stop()

df = st.session_state.raw_df

# --------------------------------------------------
# Run quality analysis with Lottie Animation
# --------------------------------------------------
# This URL is a "Data Scanning" animation
LOTTIE_URL = "https://assets5.lottiefiles.com/packages/lf20_f1c5O2.json"

with display_lottie_spinner(LOTTIE_URL, "Scanning Data Structure..."):
    report = analyze_quality(df)
    st.session_state.quality_report = report

st.success("✅ Data quality analysis complete")

# --------------------------------------------------
# High-level metrics
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rows", f"{report['rows']:,}")
col2.metric("Columns", report["columns"])
col3.metric("Missing %", f"{report['missing_%']:.2f}%")
col4.metric("Duplicates", report["duplicates"])

st.divider()

# --------------------------------------------------
# Data Tables Section (Tabs)
# --------------------------------------------------
st.subheader("📋 Detailed Data Logs")
tab1, tab2 = st.tabs(["Missing Values Table", "Data Types Table"])

with tab1:
    missing_df = (
        pd.DataFrame.from_dict(report["missing_cols"], orient="index", columns=["Missing Count"])
        .sort_values(by="Missing Count", ascending=False)
    )
    st.dataframe(missing_df, use_container_width=True)

with tab2:
    dtype_df = pd.DataFrame.from_dict(
        report["dtypes"], orient="index", columns=["Count"]
    )
    st.dataframe(dtype_df, use_container_width=True)

st.divider()

# --------------------------------------------------
# Visual Insights Section
# --------------------------------------------------
st.subheader("📊 Visual Insights")

# --- Chart 1: Data Health Map (Missing Values) ---
missing_data = pd.DataFrame.from_dict(report["missing_cols"], orient="index", columns=["Count"]).reset_index()
missing_data.columns = ['Column', 'Missing Count']
# Filter to show only columns with issues
missing_data = missing_data[missing_data['Missing Count'] > 0]

if not missing_data.empty:
    fig_bar = px.bar(
        missing_data.sort_values(by="Missing Count"), 
        x='Missing Count', 
        y='Column', 
        orientation='h',
        color='Missing Count',
        color_continuous_scale='Reds',
        template='plotly_dark',
        title="Missing Values Distribution"
    )
    fig_bar.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.success("✨ Perfect! No missing values detected in any column.")

# --- Chart 2: Column Data Types (Pie Chart) ---
# Prepare the data
dtype_visual_df = pd.DataFrame.from_dict(
    report["dtypes"], orient="index", columns=["Count"]
).reset_index()
dtype_visual_df.columns = ['Data Type', 'Count']

# ✅ Critical Fix: Convert dtypes to strings for Plotly to avoid JSON errors
dtype_visual_df['Data Type'] = dtype_visual_df['Data Type'].astype(str)

fig_pie = px.pie(
    dtype_visual_df, 
    values='Count', 
    names='Data Type', 
    hole=0.4,
    title="Data Type Distribution",
    template='plotly_dark',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_pie, use_container_width=True)

# --------------------------------------------------
# Next step hint
# --------------------------------------------------
st.info("➡️ Proceed to **Data Cleaning** from the sidebar to fix these issues.")