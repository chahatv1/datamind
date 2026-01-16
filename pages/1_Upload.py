import streamlit as st
import pandas as pd
import os
from modules.ui_components import render_sidebar_progress

# 1. Sidebar Progress
render_sidebar_progress("Upload")

st.header("📤 Upload Dataset")
st.write("Upload a CSV file or use our sample dataset to begin the DataMind analysis pipeline.")

# --- Demo Data Section (Updated to use data/sample.csv) ---
if st.button("💡 Load Sample Dataset"):
    # Define the path relative to the root directory
    file_path = "data/sample.csv"
    
    if os.path.exists(file_path):
        try:
            sample_df = pd.read_csv(file_path)
            st.session_state.raw_df = sample_df
            st.success("✅ Sample dataset loaded from 'data/sample.csv'! Proceed to Quality Analysis.")
            
            # Show a quick preview of what was loaded
            with st.expander("Peek at the sample data"):
                st.dataframe(sample_df.head(), use_container_width=True)
                
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")
    else:
        st.error("⚠️ 'data/sample.csv' not found. Please make sure the file exists in the 'data' folder.")

st.divider()

# --- File Uploader Section ---
uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.raw_df = df
        st.success("✅ File uploaded successfully")
    except Exception as e:
        st.error("❌ Failed to read the CSV file.")
        st.code(str(e))

# --- Data Preview ---
if st.session_state.raw_df is not None:
    df = st.session_state.raw_df
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head(50), use_container_width=True)
    st.info("➡️ Proceed to **Quality Analysis** using the sidebar to continue.")
else:
    st.warning("Please upload a CSV file or click 'Load Sample Dataset' to continue.")