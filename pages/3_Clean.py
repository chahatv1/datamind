import streamlit as st

from modules.data_cleaner import clean_data
from modules.advanced_cleaner import smart_clean

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
# Cleaning options (MVP: auto)
# --------------------------------------------------
st.subheader("⚙️ Cleaning Strategy")

use_advanced = st.checkbox(
    "Use advanced cleaning (outlier removal, high-missing columns)",
    value=True
)

# --------------------------------------------------
# Run cleaning
# --------------------------------------------------
if st.button("🚀 Clean Data"):
    with st.spinner("Cleaning data..."):
        if use_advanced:
            clean_df = smart_clean(raw_df, report)
        else:
            clean_df = clean_data(raw_df, report)

        st.session_state.clean_df = clean_df

    st.success("✅ Data cleaning complete")

    # --------------------------------------------------
    # Before vs After Metrics
    # --------------------------------------------------
    st.subheader("📊 Before vs After")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows (Before)", raw_df.shape[0])
        st.metric("Columns (Before)", raw_df.shape[1])

    with col2:
        st.metric("Rows (After)", clean_df.shape[0])
        st.metric("Columns (After)", clean_df.shape[1])

    # --------------------------------------------------
    # Preview cleaned data
    # --------------------------------------------------
    st.subheader("🔍 Cleaned Data Preview")
    st.dataframe(clean_df.head(50), use_container_width=True)

    st.info("➡️ Proceed to **Analysis** to discover patterns and anomalies.")
else:
    st.info("Click **Clean Data** to apply fixes.")
