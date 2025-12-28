import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    """ML-based anomaly detection"""
    anomalies = {}
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        preds = iso_forest.fit_predict(df[numeric_cols])
        anomalies['count'] = sum(preds == -1)
        anomalies['anomaly_rows'] = df[preds == -1].index.tolist()
    
    return anomalies

def test():
    df = pd.DataFrame({'sales': [100, 120, 110, 9999, 115]})
    return detect_anomalies(df)
