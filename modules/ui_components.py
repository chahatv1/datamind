import streamlit as st
import requests
from streamlit_lottie import st_lottie
from contextlib import contextmanager  

def render_sidebar_progress(current_page_name):
    """Renders a consistent sidebar with a progress bar across all pages."""
    steps = ["Upload", "Quality", "Clean", "Analysis", "Story", "Reports"]
    
    page_map = {
        "Home": 0, "Upload": 1, "Quality": 2, 
        "Clean": 3, "Analysis": 4, "Story": 5, "Reports": 6
    }
    
    current_idx = page_map.get(current_page_name, 0)
    
    st.sidebar.header("🧠 DataMind Pipeline")
    progress = current_idx / (len(steps))
    st.sidebar.write(f"**Progress: {int(progress * 100)}%**")
    st.sidebar.progress(progress)
    st.sidebar.divider()

def load_lottie_url(url: str):
    """Downloads a Lottie animation from a URL."""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

@contextmanager  
def display_lottie_spinner(lottie_url, text="Processing..."):
    """
    A context manager that displays a Lottie animation instead of a spinner.
    Usage:
        with display_lottie_spinner(url, "Analyzing..."):
            long_running_function()
    """
    # 1. Load the animation
    lottie_json = load_lottie_url(lottie_url)
    
    # 2. Create a placeholder container
    placeholder = st.empty()
    
    # 3. Render the animation inside the placeholder
    with placeholder.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            if lottie_json:
                st_lottie(lottie_json, height=150, key="loading_anim")
            else:
                st.spinner(text)
        with col2:
            st.markdown(f"### 🤖 {text}")
            st.caption("Our AI models are scanning your data...")
            
    # 4. Yield control back to the main program
    try:
        yield
    finally:
        # 5. Clear the animation once the work is done
        placeholder.empty()