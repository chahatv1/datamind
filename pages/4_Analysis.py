import streamlit as st
import pandas as pd

from modules.pattern_analyzer import find_patterns
from modules.anomaly_detector import detect_anomalies

st.header("📊 Data Analysis & Pattern Detection")

# --------------------------------------------------
# Guards
# --------------------------------------------------
if st.session_state.clean_df is None:
    st.warning("⚠️ Cleaned data not found. Please complete data cleaning first.")
    st.stop()

df = st.session_state.clean_df

# --------------------------------------------------
# Run analysis
# --------------------------------------------------
with st.spinner("Analyzing patterns and detecting anomalies..."):
    patterns = find_patterns(df)
    anomalies = detect_anomalies(df)

    st.session_state.patterns = patterns
    st.session_state.anomalies = anomalies

st.success("✅ Analysis complete")

st.divider()

# --------------------------------------------------
# Numeric Summary
# --------------------------------------------------
st.subheader("📈 Numeric Column Insights")

numeric_summary = patterns.get("numeric_summary", {})

if numeric_summary:
    numeric_df = pd.DataFrame(numeric_summary).T
    numeric_df = numeric_df.rename(columns={
        "mean": "Mean",
        "std": "Std Dev",
        "outliers": "Outlier Count"
    })
    st.dataframe(numeric_df, use_container_width=True)
else:
    st.info("No numeric columns found.")

# --------------------------------------------------
# Top Categories
# --------------------------------------------------
st.subheader("🏷️ Top Categories")

top_categories = patterns.get("top_categories", {})

if top_categories:
    for col, values in top_categories.items():
        st.markdown(f"**{col}**")
        cat_df = pd.DataFrame(
            list(values.items()), columns=["Category", "Count"]
        )
        st.dataframe(cat_df, use_container_width=True)
else:
    st.info("No categorical columns found.")

# --------------------------------------------------
# Anomaly Summary
# --------------------------------------------------
st.subheader("🚨 Anomaly Detection")

if anomalies and anomalies.get("count", 0) > 0:
    st.metric("Anomalies Detected", anomalies["count"])
    st.write("Row indices flagged as anomalous:")
    st.code(anomalies["anomaly_rows"])
else:
    st.success("No significant anomalies detected.")

# --------------------------------------------------
# Next step hint
# --------------------------------------------------
st.info("➡️ Proceed to **Story Generation** for AI-written insights.")
