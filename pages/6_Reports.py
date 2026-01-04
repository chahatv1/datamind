import streamlit as st

st.header("📄 Reports & Exports")

# --------------------------------------------------
# Guards
# --------------------------------------------------
if st.session_state.clean_df is None:
    st.warning("⚠️ No cleaned data found. Please complete earlier steps.")
    st.stop()

clean_df = st.session_state.clean_df

# --------------------------------------------------
# Download cleaned CSV
# --------------------------------------------------
st.subheader("⬇️ Download Cleaned Dataset")

csv_data = clean_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Cleaned CSV",
    data=csv_data,
    file_name="datamind_cleaned_data.csv",
    mime="text/csv"
)

st.success("✅ Cleaned dataset ready for download")

st.divider()

# --------------------------------------------------
# Story preview (optional context)
# --------------------------------------------------
if st.session_state.story:
    st.subheader("📖 Executive Summary Preview")
    st.markdown(st.session_state.story)

# --------------------------------------------------
# Coming soon section
# --------------------------------------------------
st.subheader("🧾 Professional Reports (Coming Soon)")

st.info(
    "📌 PDF and interactive HTML report export is under development.\n\n"
    "The final report will include:\n"
    "- Executive summary\n"
    "- Data quality metrics (before & after)\n"
    "- Key insights & anomalies\n"
    "- Visualizations\n"
    "- Methodology appendix"
)
