import streamlit as st
import pandas as pd

from modules.quality_analyzer import analyze_quality

st.header("🧪 Data Quality Analysis")

# --------------------------------------------------
# Guard: Ensure data is uploaded
# --------------------------------------------------
if st.session_state.raw_df is None:
    st.warning("⚠️ No dataset found. Please upload a CSV file first.")
    st.stop()

df = st.session_state.raw_df

# --------------------------------------------------
# Run quality analysis
# --------------------------------------------------
with st.spinner("Analyzing data quality..."):
    report = analyze_quality(df)
    st.session_state.quality_report = report

st.success("✅ Data quality analysis complete")

# --------------------------------------------------
# High-level metrics
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", report["rows"])
col2.metric("Columns", report["columns"])
col3.metric("Missing %", f"{report['missing_%']:.2f}%")
col4.metric("Duplicates", report["duplicates"])

st.divider()

# --------------------------------------------------
# Missing values by column
# --------------------------------------------------
st.subheader("🧩 Missing Values by Column")

missing_df = (
    pd.DataFrame.from_dict(report["missing_cols"], orient="index", columns=["Missing Count"])
    .sort_values(by="Missing Count", ascending=False)
)

st.dataframe(missing_df, use_container_width=True)

# --------------------------------------------------
# Data types summary
# --------------------------------------------------
st.subheader("📐 Column Data Types")

dtype_df = pd.DataFrame.from_dict(
    report["dtypes"], orient="index", columns=["Count"]
)

st.dataframe(dtype_df, use_container_width=True)

# --------------------------------------------------
# Next step hint
# --------------------------------------------------
st.info("➡️ Proceed to **Data Cleaning** from the sidebar to fix these issues.")
