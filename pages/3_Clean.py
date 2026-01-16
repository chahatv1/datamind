import streamlit as st
import pandas as pd
from modules.data_cleaner import clean_data
from modules.advanced_cleaner import smart_clean
from modules.ui_components import render_sidebar_progress, display_lottie_spinner

# 1. Sidebar Progress
render_sidebar_progress("Clean")

st.header("🧹 Data Cleaning")

# --------------------------------------------------
# Guards
# --------------------------------------------------
if st.session_state.raw_df is None:
    st.warning("⚠️ No dataset found. Please upload a CSV file first.")
    st.stop()

if st.session_state.quality_report is None:
    st.warning("⚠️ Please run data quality analysis first.")
    st.stop()

raw_df = st.session_state.raw_df
report = st.session_state.quality_report

# --------------------------------------------------
# Cleaning options
# --------------------------------------------------
st.subheader("⚙️ Cleaning Strategy")

col1, col2 = st.columns([3, 1])
with col1:
    st.info("Select a strategy to automatically fix missing values, duplicates, and outliers.")
    use_advanced = st.checkbox(
        "Use Advanced Cleaning (outlier removal + smart imputation)",
        value=True
    )

# --------------------------------------------------
# Run cleaning with Animation
# --------------------------------------------------
# URL for a "Cleaning/Processing" animation
CLEAN_ANIMATION_URL = "https://assets9.lottiefiles.com/packages/lf20_Tkwjw8.json"

if st.button("🚀 Clean Data", type="primary"):
    
    with display_lottie_spinner(CLEAN_ANIMATION_URL, "Scrubbing dataset..."):
        if use_advanced:
            clean_df = smart_clean(raw_df, report)
        else:
            clean_df = clean_data(raw_df, report)

        st.session_state.clean_df = clean_df

    st.success("✅ Data cleaning complete!")

    # --------------------------------------------------
    # Before vs After Metrics
    # --------------------------------------------------
    st.divider()
    st.subheader("📊 Optimization Results")

    col1, col2, col3, col4 = st.columns(4)

    # Calculate deltas
    rows_delta = clean_df.shape[0] - raw_df.shape[0]
    cols_delta = clean_df.shape[1] - raw_df.shape[1]

    col1.metric("Original Rows", f"{raw_df.shape[0]:,}")
    col2.metric("Cleaned Rows", f"{clean_df.shape[0]:,}", delta=rows_delta)
    col3.metric("Original Cols", raw_df.shape[1])
    col4.metric("Cleaned Cols", clean_df.shape[1], delta=cols_delta)

    # --------------------------------------------------
    # Preview cleaned data
    # --------------------------------------------------
    st.subheader("🔍 Cleaned Data Preview")
    st.dataframe(clean_df.head(50), use_container_width=True)

    st.info("➡️ Proceed to **Analysis** to discover patterns and anomalies.")

else:
    # Show a placeholder state if they haven't clicked clean yet
    if st.session_state.clean_df is None:
        st.write("Click the button above to start the cleaning process.")