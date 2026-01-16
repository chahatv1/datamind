import streamlit as st
import pandas as pd
import plotly.express as px
from modules.pattern_analyzer import find_patterns
from modules.anomaly_detector import detect_anomalies
from modules.ui_components import render_sidebar_progress, display_lottie_spinner

# --- CRASH PROOFING: Initialize Session State ---
if "patterns" not in st.session_state:
    st.session_state.patterns = None
if "anomalies" not in st.session_state:
    st.session_state.anomalies = None
if "clean_df" not in st.session_state:
    st.session_state.clean_df = None

# 1. Sidebar
render_sidebar_progress("Analysis")

st.header("📊 Deep Dive Analysis")

# 2. Guard
if st.session_state.clean_df is None:
    st.warning("⚠️ No cleaned data found. Please complete data cleaning first.")
    st.stop()

df = st.session_state.clean_df

# 3. Run Analysis with Animation
# URL for an "Analytics/Graph" animation
ANALYSIS_ANIMATION_URL = "https://assets8.lottiefiles.com/packages/lf20_gamjwrq2.json"

if st.session_state.patterns is None:
    with display_lottie_spinner(ANALYSIS_ANIMATION_URL, "Detecting Patterns & Anomalies..."):
        patterns = find_patterns(df)
        anomalies = detect_anomalies(df)
        st.session_state.patterns = patterns
        st.session_state.anomalies = anomalies
else:
    patterns = st.session_state.patterns
    anomalies = st.session_state.anomalies

# --- Section 1: Correlation Heatmap ---
st.subheader("🔥 Correlation Heatmap")
st.caption("Identify relationships between numerical variables.")

numeric_df = df.select_dtypes(include=['number'])

if len(numeric_df.columns) > 1:
    corr = numeric_df.corr()
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        aspect="auto",
        template='plotly_dark'
    )
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("Not enough numerical columns to generate a heatmap.")

st.divider()

# --- Section 2: Distribution Explorer ---
st.subheader("📈 Distribution Explorer")
st.caption("Visualize how your data is spread out.")

numeric_cols = numeric_df.columns.tolist()
if numeric_cols:
    selected_col = st.selectbox("Select a column to visualize:", numeric_cols)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist = px.histogram(
            df, 
            x=selected_col, 
            nbins=30, 
            title=f"{selected_col} Distribution",
            template='plotly_dark',
            color_discrete_sequence=['#6366f1']
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col2:
        fig_box = px.box(
            df, 
            y=selected_col, 
            title=f"{selected_col} Box Plot",
            template='plotly_dark',
            color_discrete_sequence=['#8b5cf6']
        )
        st.plotly_chart(fig_box, use_container_width=True)
else:
    st.info("No numerical columns found for distribution plots.")

st.divider()

# --- Section 3: Anomaly Visualization ---
st.subheader("🚨 Anomaly Detection")

if anomalies and anomalies.get("count", 0) > 0:
    st.metric("Anomalies Detected", anomalies["count"], delta="-High Risk", delta_color="inverse")
    
    if len(numeric_cols) >= 2:
        x_col = st.selectbox("X-Axis for Anomaly Plot", numeric_cols, index=0)
        y_col = st.selectbox("Y-Axis for Anomaly Plot", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
        
        plot_df = df.copy()
        plot_df['Type'] = 'Normal'
        plot_df.loc[anomalies['anomaly_rows'], 'Type'] = 'Anomaly'
        
        fig_anom = px.scatter(
            plot_df,
            x=x_col,
            y=y_col,
            color='Type',
            color_discrete_map={'Normal': '#334155', 'Anomaly': '#ef4444'},
            title="Anomaly Scatter Plot",
            template='plotly_dark',
            hover_data=plot_df.columns
        )
        st.plotly_chart(fig_anom, use_container_width=True)
    else:
        st.write("Row indices flagged as anomalous:")
        st.code(anomalies["anomaly_rows"])
else:
    st.success("✅ System Clean: No significant anomalies detected.")

st.info("➡️ Proceed to **Story Generation** for AI-written insights.")