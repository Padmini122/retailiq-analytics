import pandas as pd
import numpy as np


def engineer_features(df):
    df = df.copy()
    df['Year']      = df['invoicedate'].dt.year
    df['Month']     = df['invoicedate'].dt.month
    df['DayOfWeek'] = df['invoicedate'].dt.dayofweek
    df['Hour']      = df['invoicedate'].dt.hour
    df['IsWeekend'] = (df['DayOfWeek'] >= 5).astype(int)
    df['Quarter']   = df['invoicedate'].dt.quarter
    return df


def safe_qcut(series, q, labels):
    try:
        return pd.qcut(series, q=q, labels=labels, duplicates='drop')
    except ValueError:
        return pd.qcut(series, q=min(q, series.nunique()),
                       labels=labels[:min(q,series.nunique())-1],
                       duplicates='drop')


def build_rfm(df):
    snap = df['invoicedate'].max() + pd.Timedelta(days=1)
    rfm  = df.groupby('customer_id').agg({
        'invoicedate': lambda x: (snap - x.max()).days,
        'invoice':     'nunique',
        'revenue':     'sum'
    }).rename(columns={
        'invoicedate': 'Recency',
        'invoice':     'Frequency',
        'revenue':     'Monetary'
    })
    rfm['R_Score'] = safe_qcut(rfm['Recency'],   4, labels=[4,3,2,1])
    rfm['F_Score'] = safe_qcut(rfm['Frequency'], 4, labels=[1,2,3,4])
    rfm['M_Score'] = safe_qcut(rfm['Monetary'],  4, labels=[1,2,3,4])
    rfm['RFM_Sum'] = (rfm['R_Score'].astype(float) +
                      rfm['F_Score'].astype(float) +
                      rfm['M_Score'].astype(float))
    rfm['Segment'] = pd.cut(
        rfm['RFM_Sum'],
        bins=[2, 5, 8, 10, 12],
        labels=['Lost','At Risk','Loyal','Champions'],
        include_lowest=True)
    return rfm
