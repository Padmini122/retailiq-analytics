import streamlit as st
import sys; sys.path.append('..')
import pandas as pd
import plotly.express as px
from src.preprocess import load_and_clean
from src.features   import engineer_features, build_rfm
from src.pricing    import DynamicPricingEngine

st.set_page_config(page_title="RetailIQ", layout="wide", page_icon="📊")

@st.cache_data
def load():
    df = load_and_clean()
    df = engineer_features(df)
    return df, build_rfm(df)

df, rfm = load()

# Sidebar
st.sidebar.title("📊 RetailIQ")
year = st.sidebar.selectbox("Year", ["All",2010,2011])

# Tabs
t1,t2,t3,t4 = st.tabs([
    "📈 Overview","👥 Customers","💡 Pricing","⚠️ Dead Stock"])
