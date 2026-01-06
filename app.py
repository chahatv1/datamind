import streamlit as st

# --------------------------------------------------
# App Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="DataMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# App Header
# --------------------------------------------------
st.title("🧠 DataMind")
st.caption("AI-Powered Data Quality & Storytelling System")

st.markdown(
    """
DataMind automates the entire data intelligence pipeline —  
from **messy CSVs** to **clean insights**, **AI narratives**, and **professional reports**.
"""
)

st.divider()

# --------------------------------------------------
# Global Session State Initialization
# --------------------------------------------------
STATE_KEYS = [
    "raw_df",
    "quality_report",
    "clean_df",
    "patterns",
    "anomalies",
    "story"
]

for key in STATE_KEYS:
    if key not in st.session_state:
        st.session_state[key] = None

# --------------------------------------------------
# Instructions
# --------------------------------------------------
st.info(
    "👈 Use the sidebar to move step-by-step through the DataMind pipeline:\n\n"
    "Upload → Quality → Clean → Analyze → Story → Reports"
)
