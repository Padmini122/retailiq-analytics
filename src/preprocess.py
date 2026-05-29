import pandas as pd
import numpy as np

def load_and_clean(filepath="../data/raw/online_retail_II.csv"):
    df = pd.read_csv(filepath)
    df = df.dropna(subset=['customer_id'])
    df = df[~df['invoice'].astype(str).str.startswith('C')]
    df = df[(df['quantity'] > 0) & (df['price'] > 0)]
    df = df.drop_duplicates()
    df['invoicedate'] = pd.to_datetime(df['invoicedate'])
    df['customer_id'] = df['customer_id'].fillna(99999).astype(int)
    df['revenue'] = df['quantity'] * df['price']
    print(f"Clean dataset: {len(df):,} rows")
    return df