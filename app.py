import streamlit as st
from modules.ui_components import render_sidebar_progress

# --------------------------------------------------
# App Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="DataMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render the shared sidebar
render_sidebar_progress("Home")

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

st.markdown("""
    <style>
    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }

    /* Glassmorphism Card Style */
    div[data-testid="stMetric"], .stDataFrame, .stAlert {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px !important;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Custom Header Styling */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }

    /* Gradient Text for the Title */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#4F46E5, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🧠 DataMind</p>', unsafe_allow_html=True)