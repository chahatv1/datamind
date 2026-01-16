import pandas as pd
import numpy as np
import streamlit as st  

@st.cache_data  
def analyze_quality(df):
    """Main function - returns quality report dict"""
    report = {}
    
    report['rows'] = len(df)
    report['columns'] = len(df.columns)
    report['missing_%'] = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
    
    report['missing_cols'] = df.isnull().sum().to_dict()
    
    report['duplicates'] = df.duplicated().sum()
    
    # Convert dtypes to string to avoid JSON serialization errors later
    dtypes_dict = df.dtypes.apply(lambda x: str(x)).value_counts().to_dict()
    report['dtypes'] = dtypes_dict
    
    return report

def test():
    # ... existing test code ...
    pass