import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import streamlit as st  # <--- Import this

@st.cache_data  # <--- Add this decorator
def detect_anomalies(df):
    """ML-based anomaly detection"""
    anomalies = {}
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        # Lower contamination to 0.05 so we only flag the "weirdest" 5%
        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        preds = iso_forest.fit_predict(df[numeric_cols])
        anomalies['count'] = int(sum(preds == -1)) # Cast to int for JSON safety
        anomalies['anomaly_rows'] = df[preds == -1].index.tolist()
    
    return anomalies