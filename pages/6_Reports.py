import streamlit as st
import pandas as pd
from modules.ui_components import render_sidebar_progress
from modules.report_generator import generate_pdf_report

# 1. Sidebar Progress
render_sidebar_progress("Reports")

st.header("📄 Professional Reports")
st.write("Export your data intelligence insights into professional formats.")

# 2. Guards: Ensure we have data to report on
if st.session_state.quality_report is None:
    st.warning("⚠️ No analysis found. Please complete the pipeline steps first.")
    st.stop()

# 3. Generate Report Button
st.subheader("📥 Export Intelligence Report")

col1, col2 = st.columns([2, 1])

with col1:
    st.info("Generates a comprehensive PDF including Executive Summary, Quality Metrics, and Anomaly Detection logs.")
    
    # Check if we have a story, if not, use placeholder
    story_text = st.session_state.story if st.session_state.story else "No AI story generated yet."
    
    if st.button("🚀 Generate PDF Report"):
        with st.spinner("Compiling insights into PDF..."):
            pdf_buffer = generate_pdf_report(
                st.session_state.quality_report,
                st.session_state.patterns,
                st.session_state.anomalies,
                story_text
            )
            
            st.success("✅ Report generated successfully!")
            
            # Download Button
            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_buffer,
                file_name="DataMind_Executive_Report.pdf",
                mime="application/pdf"
            )

st.divider()

# 4. CSV Export (Existing Feature)
st.subheader("📊 Export Cleaned Data")
if st.session_state.clean_df is not None:
    csv_data = st.session_state.clean_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Cleaned CSV",
        data=csv_data,
        file_name="datamind_cleaned_data.csv",
        mime="text/csv"
    )
else:
    st.warning("Cleaned data not available.")