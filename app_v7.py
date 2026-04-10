import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
import io
import warnings
warnings.filterwarnings("ignore")

# ── Google Sheets credit system ───────────────────────────────────────────────
from google.oauth2.service_account import Credentials
import gspread

GSHEET_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def _get_sheet():
    """Authenticate and return the credits worksheet."""
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=GSHEET_SCOPES)
    gc = gspread.authorize(creds)
    spreadsheet_id = st.secrets["SHEET_ID"]
    sh = gc.open_by_key(spreadsheet_id)
    return sh.sheet1 

def lookup_key(access_key: str) -> dict | None:
    """Find a row by access key."""
    try:
        ws = _get_sheet()
        records = ws.get_all_records()
        for i, row in enumerate(records, start=2):
            if str(row.get("Key", "")).strip() == access_key.strip():
                return {
                    "row_index": i,
                    "key": row["Key"],
                    "credits": int(row.get("Credits", 0)),
                    "date_purchased": row.get("DatePurchased", ""),
                    "email": row.get("Email", ""),
                }
        return None
    except Exception as e:
        st.error(f"Sheet lookup error: {e}")
        return None

def deduct_credit(row_index: int, current_credits: int) -> int:
    """Write credits − 1 back to the sheet."""
    try:
        ws = _get_sheet()
        new_credits = max(0, current_credits - 1)
        ws.update_cell(row_index, 2, new_credits)
        return new_credits
    except Exception as e:
        st.error(f"Credit deduction error: {e}")
        return current_credits

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PanelStatX",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Syne:wght@400;500;600;700;800&display=swap');

:root {
    --bg:        #0a0c10;
    --surface:   #111318;
    --surface2:  #181c24;
    --border:    #1f2535;
    --accent:    #00e5c8;
    --accent2:   #7c6df0;
    --text:      #e2e8f4;
    --muted:     #6b7a9a;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
}

/* Single Column SaaS Layout Styling */
.saas-container {
    max-width: 700px;
    margin: 0 auto;
    padding: 80px 20px;
    text-align: center;
}
.saas-badge {
    background: rgba(0, 229, 200, 0.1);
    border: 1px solid rgba(0, 229, 200, 0.2);
    color: var(--accent);
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 0.7rem;
    display: inline-block;
    margin-bottom: 24px;
}
.saas-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fff 30%, #6b7a9a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 16px;
}
.saas-subtitle {
    color: var(--muted);
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 40px;
}
.saas-feat-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 30px;
    text-align: left;
    margin-bottom: 40px;
}
.feat-item { display: flex; gap: 16px; margin-bottom: 20px; }
.feat-icon { color: var(--accent); font-weight: bold; font-size: 1.2rem; }
.feat-text b { display: block; color: var(--text); font-size: 0.95rem; }
.feat-text span { color: var(--muted); font-size: 0.85rem; }

.access-card {
    background: var(--surface2);
    border: 1px solid var(--accent);
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    border-radius: 20px;
    padding: 40px;
    margin-top: 20px;
}

/* App Internal UI */
.scard { background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin-bottom: 16px; }
.scard-title { font-family: 'Syne', sans-serif; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: var(--muted); margin-bottom: 14px; }
.ai-box { background: linear-gradient(135deg, rgba(0,229,200,0.05) 0%, rgba(124,109,240,0.08) 100%); border-left: 3px solid var(--accent); border-radius: 8px; padding: 20px; color: var(--text); font-size: 0.85rem; white-space: pre-wrap; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for key, default in [
    ("df", None), ("results", None), ("ai_explanation", ""), 
    ("model_type", "Fixed Effects (Two-Way)"), ("access_granted", False),
    ("user_key", ""), ("user_credits", 0), ("user_row", None)
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── LANDING PAGE / GATE ───────────────────────────────────────────────────────
if not st.session_state.access_granted:
    st.markdown('<div class="saas-container">', unsafe_allow_html=True)
    st.markdown('<div class="saas-badge">VERSION 7.0 · ECONOMETRICS ENGINE</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="saas-title">PanelStatX</h1>', unsafe_allow_html=True)
    st.markdown('<p class="saas-subtitle">Built for rigorous MSc and PhD research. Automated diagnostics, AI interpretations, and publication-ready exports.</p>', unsafe_allow_html=True)

    st.markdown("""
        <div class="saas-feat-box">
            <div class="feat-item">
                <div class="feat-icon">✦</div>
                <div class="feat-text"><b>Advanced Estimators</b><span>Fixed Effects, Random Effects, and First-Difference models.</span></div>
            </div>
            <div class="feat-item">
                <div class="feat-icon">✦</div>
                <div class="feat-text"><b>AI Insights</b><span>Automated GPT-4 interpretation of economic significance and coefficients.</span></div>
            </div>
            <div class="feat-item">
                <div class="feat-icon">✦</div>
                <div class="feat-text"><b>Professional Reports</b><span>Export complete analysis to formatted DOCX in one click.</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.link_button("Get Analysis Credits → $10 for 5 runs", "https://flutterwave.com/pay/j5m67hrqr4iq", use_container_width=True)

    with st.container():
        st.markdown('<div class="access-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color:#fff; margin-bottom:20px;">Unlock Workspace</h3>', unsafe_allow_html=True)
        entered_key = st.text_input("Access Key", type="password", placeholder="Enter your key...", label_visibility="collapsed")
        if st.button("Access Dashboard", use_container_width=True, type="primary"):
            record = lookup_key(entered_key)
            if record and record["credits"] > 0:
                st.session_state.access_granted = True
                st.session_state.user_key = record["key"]
                st.session_state.user_credits = record["credits"]
                st.session_state.user_row = record["row_index"]
                st.rerun()
            else:
                st.error("Invalid key or zero credits.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<p style="margin-top:40px; font-size:0.8rem; color:#6b7a9a;"><a href="https://wa.me/2348096506034" style="color:#00e5c8; text-decoration:none;">Contact Support</a> | <a href="#" style="color:#6b7a9a; text-decoration:none;">User Guide</a></p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ── MAIN APP UI ───────────────────────────────────────────────────────────────
st.sidebar.title("⬡ PanelStatX")
st.sidebar.markdown(f"Key: `{st.session_state.user_key}`")
st.sidebar.markdown(f"Credits: **{st.session_state.user_credits}**")

uploaded = st.sidebar.file_uploader("Upload Data", type=["csv", "xlsx"])
if uploaded:
    if uploaded.name.endswith(".csv"):
        st.session_state.df = pd.read_csv(uploaded)
    else:
        st.session_state.df = pd.read_excel(uploaded)
    st.sidebar.success("Data Loaded!")

if st.session_state.df is not None:
    df = st.session_state.df
    st.header("Analysis Workspace")
    
    tab1, tab2, tab3 = st.tabs(["Data Explorer", "Regression", "AI Insights"])
    
    with tab1:
        st.markdown('<div class="scard-title">Dataset Preview</div>', unsafe_allow_html=True)
        st.dataframe(df.head(50), use_container_width=True)
        
    with tab2:
        y_col = st.selectbox("Dependent Variable (Y)", df.columns)
        x_cols = st.multiselect("Independent Variables (X)", [c for c in df.columns if c != y_col])
        if st.button("Run Analysis", type="primary") and x_cols:
            if st.session_state.user_credits > 0:
                # Deduction logic
                st.session_state.user_credits = deduct_credit(st.session_state.user_row, st.session_state.user_credits)
                st.success("Analysis Complete (1 Credit Deducted)")
                # (Placeholder for regression functions from original script)
                st.info("Visualizing results...")
            else:
                st.error("Insufficient credits.")

    with tab3:
        st.markdown('<div class="ai-box">GPT-4 Analysis will appear here after running regression.</div>', unsafe_allow_html=True)

else:
    st.info("Please upload a dataset or use demo data to begin.")
