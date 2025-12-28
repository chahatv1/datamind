import pandas as pd
import numpy as np

def smart_clean(df, quality_report):
    """Advanced cleaning based on quality issues"""
    df_clean = df.copy()
    
    # 1. Remove high-missing columns (>50%)
    missing_cols = quality_report.get('missing_cols', {})
    for col, missing_count in missing_cols.items():
        if missing_count / len(df) > 0.5:
            df_clean = df_clean.drop(columns=[col])
    
    # 2. Outlier removal (IQR method)
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df_clean = df_clean[(df_clean[col] >= lower) & (df_clean[col] <= upper)]
    
    return df_clean

def test():
    df = pd.DataFrame({'sales': [100, 200, 9999, 150], 'bad_col': [None]*3 + [1]})
    report = {'missing_cols': {'bad_col': 3}}
    return smart_clean(df, report).to_dict()