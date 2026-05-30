import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import plotly.express as px
import urllib.request

# Keep your path setup clean so internal modules can be imported smoothly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocess import load_and_clean
from src.features import engineer_features, build_rfm
from src.pricing import DynamicPricingEngine

# ═══ DATA LOADING WITH CACHING ═══

@st.cache_data
def load_data():
    """
    Checks for the dataset locally first. If missing (like on Streamlit Cloud),
    downloads the file to the local disk workspace using an unblocked high-speed 
    mirror, then processes it.
    """
    # 1. Define paths for your local machine structure
    current_dir = Path(__file__).parent
    local_data_path = (current_dir / ".." / "data" / "raw" / "online_retail_II.csv").resolve()
    
    # 2. Define the target path inside the Streamlit Cloud container
    cloud_data_path = os.path.join(os.getcwd(), "online_retail_II.csv")
    
    # 3. Determine if we can use the local machine file
    if os.path.exists(local_data_path):
        final_filepath = str(local_data_path)
    # 4. Determine if it was already downloaded to the cloud server disk
    elif os.path.exists(cloud_data_path):
        final_filepath = cloud_data_path
    # 5. Safe Fallback: Download the file to the disk so Pandas can read it locally
    else:
        # A completely open, high-speed cloud mirror that allows raw downloads
        unblocked_url = "https://huggingface.co/datasets/as-cle-data/online-retail-ii/resolve/main/online_retail_II.csv"
        
        with st.spinner("Downloading dataset to cloud server storage... Please wait, this takes a moment."):
            # Add basic browser headers to be absolutely safe against infrastructure firewalls
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
            urllib.request.install_opener(opener)
            
            # Download and save the file physically to the cloud server disk
            urllib.request.urlretrieve(unblocked_url, cloud_data_path)
            
        final_filepath = cloud_data_path

    # Pass the verified local physical file path to your cleaning pipeline
    df = load_and_clean(filepath=final_filepath)
    df = engineer_features(df)
    rfm = build_rfm(df)
    
    return df, rfm

# Call the cached data function cleanly
df, rfm = load_data()


# ═══ SIDEBAR ═══
st.sidebar.title("📊 RetailIQ")
st.sidebar.caption("Smart Retail Analytics · Thiranex Internship")
year = st.sidebar.selectbox("Year", ["All", 2010, 2011])

# Apply year filter safely
d = df if year == "All" else df[df['Year'] == year]


# ═══ TABS INITIALIZATION ═══
t1, t2, t3, t4 = st.tabs([
    "📈 Overview", "👥 Customers", "💡 Pricing Engine", "⚠️ Dead Stock"
])


# ═══ TAB 1: OVERVIEW ═══
with t1:
    st.header("Business Overview")
    a, b, c, e = st.columns(4)
    a.metric("💰 Revenue",   f"£{d['revenue'].sum():,.0f}")
    b.metric("🛒 Orders",    f"{d['invoice'].nunique():,}")
    c.metric("👤 Customers", f"{d['customer_id'].nunique():,}")
    e.metric("💎 Avg Order", f"£{d.groupby('invoice')['revenue'].sum().mean():,.2f}")

    monthly = d.groupby(['Year','Month'])['revenue'].sum().reset_index()
    monthly['Period'] = monthly['Year'].astype(str) + '-' + monthly['Month'].astype(str).str.zfill(2)
    fig = px.area(monthly, x='Period', y='revenue',
                  title='Monthly Revenue Trend',
                  color_discrete_sequence=['#ff4d00'])
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        top10 = (d.groupby('description')['revenue']
                 .sum().sort_values(ascending=False)
                 .head(10).reset_index())
        fig2 = px.bar(top10, x='revenue', y='description',
                      orientation='h', title='Top 10 Products',
                      color_discrete_sequence=['#1a56db'])
        fig2.update_layout(yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        country = d.groupby('country')['revenue'].sum().reset_index()
        fig3 = px.bar(country.sort_values('revenue', ascending=False).head(8),
                      x='country', y='revenue', title='Revenue by Country',
                      color_discrete_sequence=['#00875a'])
        st.plotly_chart(fig3, use_container_width=True)


# ═══ TAB 2: CUSTOMERS ═══
with t2:
    st.header("Customer Segments")
    seg = rfm['Segment'].value_counts().reset_index()
    seg.columns = ['Segment', 'Count']
    col1, col2 = st.columns(2)
    with col1:
        fig4 = px.pie(seg, values='Count', names='Segment',
                      title='RFM Customer Segments', hole=0.5,
                      color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig4, use_container_width=True)
    with col2:
        st.subheader("Segment Summary")
        st.dataframe(rfm.groupby('Segment')[['Recency','Frequency','Monetary']]
                     .mean().round(1), use_container_width=True)


# ═══ TAB 3: PRICING ENGINE ═══
with t3:
    st.header("💡 Dynamic Pricing Engine")
    st.caption("Find the optimal discount to maximise revenue before dead-stock deadline.")
    c1, c2, c3 = st.columns(3)
    cat   = c1.selectbox("Category", ['Home Decor','Gifts','Kitchen','Seasonal','Stationery'])
    price = c1.number_input("Current Price (£)", value=4.95, step=0.05)
    stock = c2.number_input("Stock Units", value=240, min_value=1)
    days  = c2.number_input("Days to Deadline", value=21, min_value=1)
    rate  = c3.number_input("Avg Daily Sales", value=8, min_value=1)

    if c3.button("🚀 Get Recommendation", type="primary"):
        r = DynamicPricingEngine(cat).recommend(price, stock, days, rate)
        st.success(f"✅ Optimal price: £{r['optimal_price']} ({r['discount_pct']}% discount)")
        r1, r2, r3 = st.columns(3)
        r1.metric("Optimal Price", f"£{r['optimal_price']}")
        r2.metric("Discount",      f"{r['discount_pct']}%")
        r3.metric("Revenue Gain",  f"£{r['revenue_gain']:+,.0f}")


# ═══ TAB 4: DEAD STOCK ═══
with t4:
    st.header("⚠️ Dead-Stock Early Warning")
    st.caption("Products that haven't sold recently — at risk of inventory loss.")
    last_sale = d.groupby('description')['invoicedate'].max()
    latest    = d['invoicedate'].max()
    days_unsold = ((latest - last_sale).dt.days).reset_index()
    days_unsold.columns = ['Product', 'Days Unsold']
    days_unsold = days_unsold.sort_values('Days Unsold', ascending=False).head(20)

    def risk(x):
        if x > 45: return '🔴 Critical'
        elif x > 30: return '🟡 Medium'
        else: return '🟢 Watch'

    days_unsold['Risk Level'] = days_unsold['Days Unsold'].apply(risk)
    st.dataframe(days_unsold, use_container_width=True)

    fig5 = px.bar(days_unsold.head(10), x='Days Unsold', y='Product',
                  orientation='h', color='Days Unsold',
                  color_continuous_scale='Reds',
                  title='Top 10 Dead-Stock Risk Products')
    fig5.update_layout(yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig5, use_container_width=True)