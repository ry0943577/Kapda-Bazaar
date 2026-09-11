import streamlit as st
import pandas as pd
import plotly.express as px
import time
import base64
import os

# --- Page Configuration ---
st.set_page_config(page_title="Kapda Bazaar - B2B Marketplace", layout="wide", initial_sidebar_state="collapsed")

# --- FUNCTION TO LOAD IMAGE (FIXED) ---
def get_base64_image(image_path):
    # Streamlit Cloud par path ka issue na aaye isliye absolute path use kar rahe hain
    try:
        # Check relative path first
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        
        # Check absolute path
        abs_path = os.path.join(os.path.dirname(__file__), image_path)
        if os.path.exists(abs_path):
            with open(abs_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        pass
    return ""

logo_base64 = get_base64_image("logo.png")

# Naya function Local Images ke liye
def get_local_img_uri(filename):
    b64 = get_base64_image(filename)
    if b64:
        ext = "jpeg" if filename.lower().endswith(("jpg", "jpeg")) else "png"
        return f"data:image/{ext};base64,{b64}"
    # Agar image save karna bhul gaye ya naam galat hua, toh ye temporary grey box dikhayega
    return "https://dummyimage.com/400x400/cccccc/000000&text=Missing+"+filename

# --- SPLASH SCREEN LOGIC ---
if 'splash_shown' not in st.session_state:
    st.session_state.splash_shown = True
    splash = st.empty()
    if logo_base64:
        splash_content = f'<img src="data:image/png;base64,{logo_base64}" style="width: 250px; animation: pulse 1.2s infinite ease-in-out;">'
    else:
        splash_content = '<h1 style="color: black; animation: pulse 1.2s infinite;">🧶 Kapda Bazaar</h1>'
        
    splash.markdown(f"""
        <style>
        @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} 100% {{ transform: scale(1); }} }}
        </style>
        <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: white; z-index: 999999999; display: flex; justify-content: center; align-items: center;">
            {splash_content}
        </div>
    """, unsafe_allow_html=True)
    time.sleep(2)
    splash.empty()

# --- CUSTOM CSS ---
st.markdown("""
<style>
.stApp { background-color: #EAEDED !important; }
header[data-testid="stHeader"] { display: none !important; }

/* Force ALL text to be black (Dark Mode Fix) */
.block-container h1, .block-container h2, .block-container h3, .block-container h4, .block-container h5, .block-container h6, .block-container p, .block-container label p, .block-container span { 
    color: #0F1111 !important; 
}

/* Tabs Fix */
button[data-baseweb="tab"] p, button[data-baseweb="tab"] span, button[data-baseweb="tab"] div { color: #131921 !important; font-weight: 800 !important; font-size: 16px !important; }
button[data-baseweb="tab"][aria-selected="true"] p, button[data-baseweb="tab"][aria-selected="true"] span, button[data-baseweb="tab"][aria-selected="true"] div { color: #B12704 !important; }
button[data-baseweb="tab"][aria-selected="true"] { border-bottom-color: #FF9900 !important; }

/* Fix for Metrics */
[data-testid="stMetricValue"] div, [data-testid="stMetricValue"] { color: #000000 !important; }
[data-testid="stMetricLabel"] p, [data-testid="stMetricLabel"] { color: #555555 !important; }

/* Float Search Bar */
div[data-testid="stTextInput"]:first-of-type { position: fixed !important; top: 10px !important; left: 24vw !important; width: 48vw !important; z-index: 99999999 !important; }
div[data-testid="stTextInput"] div[data-baseweb="input"] { background-color: #FFFFFF !important; border: 3px solid #FEBD69 !important; border-radius: 6px !important; }
div[data-testid="stTextInput"] input { color: #0F1111 !important; background-color: #FFFFFF !important; -webkit-text-fill-color: #0F1111 !important; font-size: 15px !important; padding: 12px !important; }

/* Layout Padding */
.block-container { padding-top: 130px !important; max-width: 100%; padding-left: 2rem !important; padding-right: 2rem !important; }

/* Header Base Styles */
.amazon-header-container { position: fixed; top: 0; left: 0; width: 100vw; z-index: 999999; }
.amazon-header-main { background-color: #131921; height: 60px; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; box-sizing: border-box; }
.amazon-header-main * { color: white !important; }
.nav-locator { display: flex; align-items: center; margin-left: 10px; cursor: pointer; padding: 5px; border: 1px solid transparent; }
.nav-locator:hover { border: 1px solid white; border-radius: 2px; }
.nav-right { display: flex; gap: 15px; align-items: center; }
.nav-right > div { cursor: pointer; padding: 8px 5px; border: 1px solid transparent; }
.nav-right > div:hover { border: 1px solid white; border-radius: 2px; }

/* Sub Header */
.amazon-header-sub { background-color: #232F3E; height: 40px; display: flex; align-items: center; padding: 0 20px; color: white; font-family: Arial, sans-serif; font-size: 14px; gap: 15px; box-sizing: border-box; }
.amazon-header-sub div { cursor: pointer; padding: 5px 8px; color: white !important; border: 1px solid transparent; }
.amazon-header-sub div:hover { border: 1px solid white; border-radius: 2px; }

/* Product Cards */
[data-testid="stVerticalBlockBorderWrapper"] { background-color: #FFFFFF !important; border: 1px solid #D5D9D9; border-radius: 8px; }
.stButton>button { background-color: #FFD814 !important; color: #0F1111 !important; border: 1px solid #FCD200 !important; border-radius: 100px !important; padding: 4px 10px; font-size: 14px; box-shadow: 0 2px 5px rgba(213,217,217,.5); width: 100%; }
.stButton>button:hover { background-color: #F7CA00 !important; border-color: #F2C200 !important; }
</style>
""", unsafe_allow_html=True)

# Generate Header Logo
if logo_base64:
    header_logo = f'<img src="data:image/png;base64,{logo_base64}" style="height: 45px; background-color: white; padding: 2px; border-radius: 5px; cursor: pointer;">'
else:
    header_logo = '<h2 style="margin: 0; cursor: pointer; font-size: 24px;">🧶 Kapda Bazaar</h2>'

# ==========================================
# ACTUAL SEARCH BAR
# ==========================================
search_query = st.text_input("", placeholder="🔍 Search Kapda Bazaar (Type to find Yarn, Mills, or Specs)", label_visibility="collapsed")

# --- FULL WIDTH FIXED HEADER ---
st.markdown(f"""
<div class="amazon-header-container">
<div class="amazon-header-main">
<div style="display: flex; align-items: center;">
{header_logo}
<div class="nav-locator">
<span style="font-size: 20px; margin-right: 5px;">📍</span>
<div style="line-height: 1.1;">
<span style="font-size: 12px; color: #CCCCCC !important;">Deliver to Rohan</span><br>
<span style="font-weight: bold; font-size: 14px;">Rau 453331</span>
</div>
</div>
</div>
<!-- Space for the floated search bar -->
<div style="width: 50vw;"></div> 
<div class="nav-right">
<div style="display: flex; align-items: center; gap: 5px;"><span style="font-size: 16px;">🇮🇳</span><span style="font-weight: bold; font-size: 14px;">EN ▾</span></div>
<div style="line-height: 1.1;"><span style="font-size: 12px;">Hello, Rohan</span><br><span style="font-weight: bold; font-size: 14px;">Account & Lists ▾</span></div>
<div style="line-height: 1.1;"><span style="font-size: 12px;">Returns</span><br><span style="font-weight: bold; font-size: 14px;">& Orders</span></div>
<div style="display: flex; align-items: flex-end; font-weight: bold; font-size: 15px;">
<span style="font-size: 24px; margin-right: 2px;">🛒</span><span style="color:#F3A847 !important; position: absolute; margin-top: -10px; margin-left: 12px;">0</span>Cart
</div>
</div>
</div>
<div class="amazon-header-sub">
<div style="font-weight: bold; font-size: 15px;">☰ All</div>
<div>Fresh Yarn</div><div>Supplier Service</div><div>Kapda Bazaar Fulfilled</div><div>Sell</div><div>Escrow Pay</div><div>Dashboard</div>
</div>
</div>
""", unsafe_allow_html=True)

# --- LOCAL IMAGES LOGIC (UPDATED TO GITHUB RAW URLS) ---
cotton_img = "https://raw.githubusercontent.com/ry0943577/Kapda-Bazaar/main/cotton.png"
poly_img = "https://raw.githubusercontent.com/ry0943577/Kapda-Bazaar/main/polyester.png"
viscose_img = "https://raw.githubusercontent.com/ry0943577/Kapda-Bazaar/main/viscose.png"
silk_img = "https://raw.githubusercontent.com/ry0943577/Kapda-Bazaar/main/silk.png"

all_products = [
    {"category": "Cotton", "mill": "Vardhman Textiles", "product": "Cotton Yarn 30s Combed", "price": 245, "score": 96, "orders": "1,240", "delivery": 3, "moq": "500", "img": cotton_img},
    {"category": "Cotton", "mill": "Trident Group", "product": "Organic Cotton 40s", "price": 280, "score": 92, "orders": "850", "delivery": 5, "moq": "1000", "img": cotton_img},
    {"category": "Cotton", "mill": "RSWM Limited", "product": "Recycled Cotton Yarn", "price": 230, "score": 94, "orders": "2,100", "delivery": 2, "moq": "2000", "img": cotton_img},
    {"category": "Cotton", "mill": "Banswara Syntex", "product": "Dyed Cotton Yarn", "price": 275, "score": 89, "orders": "670", "delivery": 6, "moq": "500", "img": cotton_img},
    {"category": "Polyester", "mill": "Nitin Spinners", "product": "Polyester Cotton Blend", "price": 210, "score": 88, "orders": "420", "delivery": 7, "moq": "300", "img": poly_img},
    {"category": "Polyester", "mill": "Reliance Tex", "product": "100% Polyester Spun", "price": 160, "score": 91, "orders": "3,400", "delivery": 3, "moq": "1000", "img": poly_img},
    {"category": "Viscose", "mill": "Aarti International", "product": "Viscose Yarn 20s", "price": 190, "score": 85, "orders": "310", "delivery": 4, "moq": "500", "img": viscose_img},
    {"category": "Viscose", "mill": "Grasim Ind.", "product": "Rayon Blended Yarn", "price": 205, "score": 95, "orders": "1,150", "delivery": 5, "moq": "800", "img": viscose_img},
    {"category": "Silk", "mill": "Mysore Silk Mill", "product": "Premium Mulberry Silk", "price": 1250, "score": 98, "orders": "120", "delivery": 7, "moq": "50", "img": silk_img},
    {"category": "Silk", "mill": "Bhagalpur Looms", "product": "Tussar Silk Yarn", "price": 950, "score": 86, "orders": "340", "delivery": 6, "moq": "100", "img": silk_img},
    {"category": "Cotton", "mill": "Arvind Mills", "product": "Denim Weaving Yarn", "price": 260, "score": 97, "orders": "4,500", "delivery": 3, "moq": "3000", "img": cotton_img},
    {"category": "Polyester", "mill": "Sutlej Textiles", "product": "Acrylic Blended Poly", "price": 185, "score": 82, "orders": "290", "delivery": 8, "moq": "400", "img": poly_img},
]

# --- TABS ---
tab_marketplace, tab_dashboard, tab_escrow = st.tabs(["🛍️ B2B Marketplace", "📈 Supplier Seller Central", "🛡️ Escrow & Trust"])

# ==========================================
# 1. MARKETPLACE TAB 
# ==========================================
with tab_marketplace:
    filter_col, product_col = st.columns([1, 4])

    with filter_col:
        with st.container(border=True):
            st.markdown("### Filters")
            st.markdown("**Categories**")
            cat_cotton = st.checkbox("Cotton Yarn", value=True)
            cat_poly = st.checkbox("Polyester Yarn", value=True)
            cat_viscose = st.checkbox("Viscose Yarn", value=True)
            cat_silk = st.checkbox("Silk Yarn", value=True)
            
            st.markdown("<br>**Price (₹/kg)**", unsafe_allow_html=True)
            price_range = st.slider("", 100, 1500, (100, 1500), label_visibility="collapsed")
            
            st.markdown("<br>**Verified Mill Score**", unsafe_allow_html=True)
            score_filter = st.radio("", ["All Scores", "⭐⭐⭐⭐⭐ 90+ Score", "⭐⭐⭐⭐ 80+ Score"], label_visibility="collapsed")
            
            st.markdown("<br>**Delivery Time**", unsafe_allow_html=True)
            del_3 = st.checkbox("Get it in 3 Days (Fast)")
            del_7 = st.checkbox("Get it in 7 Days")

    filtered_products = []
    for p in all_products:
        if search_query and search_query.lower() not in p['product'].lower() and search_query.lower() not in p['mill'].lower() and search_query.lower() not in p['category'].lower():
            continue
        if p['category'] == "Cotton" and not cat_cotton: continue
        if p['category'] == "Polyester" and not cat_poly: continue
        if p['category'] == "Viscose" and not cat_viscose: continue
        if p['category'] == "Silk" and not cat_silk: continue
        if not (price_range[0] <= p['price'] <= price_range[1]): continue
        if "90+" in score_filter and p['score'] < 90: continue
        if "80+" in score_filter and p['score'] < 80: continue
        if del_3 and p['delivery'] > 3: continue
        if del_7 and p['delivery'] > 7: continue
        filtered_products.append(p)

    with product_col:
        if not any([cat_cotton, cat_poly, cat_viscose, cat_silk]):
            st.error("⚠️ You have unchecked all categories. Please select at least one to see products.")
        elif len(filtered_products) == 0:
            st.warning("No products found matching your filters. Try adjusting the search or price.")
        else:
            st.markdown(f"**Showing {len(filtered_products)} Results**")
            for i in range(0, len(filtered_products), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(filtered_products):
                        p = filtered_products[i+j]
                        with cols[j]:
                            with st.container(border=True):
                                st.markdown(f"<div style='height: 160px; overflow: hidden; border-radius: 4px; margin-bottom: 10px;'><img src='{p['img']}' style='width: 100%; height: 100%; object-fit: cover;'></div>", unsafe_allow_html=True)
                                st.markdown(f"<span style='font-size: 18px; color: #007185 !important; font-weight: 500;'>{p['product']}</span>", unsafe_allow_html=True)
                                st.markdown(f"<span style='font-size: 14px; color: #565959 !important;'>by {p['mill']}</span>", unsafe_allow_html=True)
                                st.markdown(f"⭐⭐⭐⭐⭐ <span style='color: #007185 !important; font-size: 14px;'>{p['score']} Mill Score </span> <span style='font-size: 12px; color: #565959 !important;'>({p['orders']})</span>", unsafe_allow_html=True)
                                st.markdown(f"<h2 style='color: #B12704 !important; margin-top: 5px; margin-bottom: 0px;'>₹{p['price']} <span style='font-size: 14px; color: #565959 !important; font-weight: normal;'>/ kg</span></h2>", unsafe_allow_html=True)
                                st.markdown(f"<span style='color: #007185 !important; font-weight: bold; font-size: 13px;'>✓ Kapda Bazaar Verified</span><br><span style='font-size: 13px; color: #0F1111 !important;'>Get it in <b>{p['delivery']} Days</b></span>", unsafe_allow_html=True)
                                st.markdown(f"<span style='font-size: 13px; color: #0F1111 !important;'>MOQ: {p['moq']} kg</span>", unsafe_allow_html=True)
                                st.markdown("<br>", unsafe_allow_html=True)
                                st.button("Add to Cart", key=f"btn_{i}_{j}")

# ==========================================
# 2. SELLER DASHBOARD
# ==========================================
with tab_dashboard:
    with st.container(border=True):
        st.title("📈 Supplier 'Seller Central' & Demand")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Market Demand Forecast")
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug (Predicted)']
            demand = [120, 135, 110, 150, 165, 180, 175, 220]
            df_demand = pd.DataFrame({'Month': months, 'Demand (Tons)': demand})
            
            fig = px.line(df_demand, x='Month', y='Demand (Tons)', markers=True)
            fig.update_layout(template="plotly_white", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='black'))
            fig.add_vrect(x0="Jul", x1="Aug (Predicted)", fillcolor="yellow", opacity=0.2, line_width=0)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("Your Mill's Performance")
            st.metric(label="Quality Consistency Score", value="96/100", delta="+2% from last month")
            st.metric(label="On-time Delivery", value="98.2%", delta="Excellent")
            st.metric(label="Capacity Utilisation", value="78%", delta="Action required: Increase production")

# ==========================================
# 3. ESCROW TAB
# ==========================================
with tab_escrow:
    with st.container(border=True):
        st.title("🛡️ Secure Payments & B2B Credit")
        st.markdown("### How our Escrow Works:")
        steps = ["1. Buyer Pays to Escrow", "2. Mill Ships Yarn", "3. Quality Verified", "4. Mill Receives Payment"]
        current_step = st.radio("Live Order #ORD-88392 Tracker:", steps, index=1)
        st.progress((steps.index(current_step) + 1) * 25)
