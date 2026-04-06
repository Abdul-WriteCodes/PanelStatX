import streamlit as st
import pandas as pd
from gsheet import find_key_row

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="PanelStatX", page_icon="📊", layout="wide")


# -----------------------------
# HEADER (reusable)
# -----------------------------
def show_header():
    st.markdown(
        """
        <div style='text-align:center;'>
            <h1> PanelStatX </h1>
            <p style='font-size:16px; color:gray; font-weight:600'>
                Panel Data Analysis Made Simple
            </p>
            <p style='font-size:14px; color:#2ECC71; text-align:center; font-weight:600'>
                🎯 Upload Data • 📝 Select Model • 🔄 Analyse • ✅ Download Results
            </p>
        </div>

        <div style='text-align:center;'>
            <p style='font-size:16px; color:gray; font-weight:600'>
                Supports Panel Regression for Different Datasets:
            </p>
            <p style='font-size:14px; color:cyan; text-align:center; font-weight:600'>
                🏙️ Companies • 🌍 Countries • 🏭 Industries • 📊 Any panel data structure
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")


# -----------------------------
# PAYMENT PROMPT
# -----------------------------
def show_payment_prompt():
    """Shows the Flutterwave payment CTA."""
    st.markdown(
        """
        <div style='background-color:#1a1a2e; padding:20px; border-radius:12px; text-align:center;'>
            <h3 style='color:#2ECC71;'>💳 Get Your Access Key</h3>
            <p style='color:gray;'>Choose a plan and get your unique key instantly after payment.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📦 Available Plans")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **🥉 Starter**
        - 10 analyses
        - ₦2,000
        """)
        st.link_button("Buy Starter", "https://flutterwave.com/pay/YOUR_LINK_HERE", use_container_width=True)

    with col2:
        st.markdown("""
        **🥈 Standard**
        - 30 analyses
        - ₦5,000
        """)
        st.link_button("Buy Standard", "https://flutterwave.com/pay/YOUR_LINK_HERE", use_container_width=True)

    with col3:
        st.markdown("""
        **🥇 Pro**
        - 100 analyses
        - ₦15,000
        """)
        st.link_button("Buy Pro", "https://flutterwave.com/pay/YOUR_LINK_HERE", use_container_width=True)

    st.caption("After payment, you'll receive your unique access key via email within minutes.")


# -----------------------------
# ACCESS CONTROL
# -----------------------------
def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.access_key = None
        st.session_state.credits = 0

    if not st.session_state.authenticated:
        show_header()

        st.markdown("## Get Ready for Analysis")
        st.caption("🔐 Enter your access key below. Don't have one? Purchase a plan to get started.")

        user_key = st.text_input("Access Key", type="password", placeholder="PSX-XXXX-XXXXXXXX")

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Unlock", use_container_width=True):
                if not user_key.strip():
                    st.error("Please enter an access key.")
                else:
                    with st.spinner("Verifying key..."):
                        row_num, row_data = find_key_row(user_key.strip())

                    if row_data is None:
                        st.error("❌ Access key not found. Please check and try again.")

                    elif str(row_data["status"]).strip().lower() == "blocked":
                        st.error("🚫 This key has been blocked. Your credits are exhausted.")
                        st.info("👇 Purchase a new plan to continue.")
                        show_payment_prompt()

                    elif int(row_data["credits"]) <= 0:
                        st.error("⚠️ No credits remaining on this key.")
                        st.info("👇 Purchase a new plan to continue.")
                        show_payment_prompt()

                    else:
                        # ✅ Valid key with credits
                        st.session_state.authenticated = True
                        st.session_state.access_key = user_key.strip()
                        st.session_state.credits = int(row_data["credits"])
                        st.rerun()

        st.markdown("---")
        show_payment_prompt()
        st.stop()


check_auth()


# -----------------------------
# MAIN APP (only runs if authenticated)
# -----------------------------
show_header()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 👤 Your Session")
    st.markdown(f"**Key:** `{st.session_state.access_key[:8]}...`")
    st.markdown(f"**Credits Remaining:** `{st.session_state.credits}`")
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.access_key = None
        st.session_state.credits = 0
        st.rerun()


# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload your dataset (CSV or Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file:
    file_name = uploaded_file.name

    try:
        # Detect file type
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        else:
            st.error("Unsupported file format")
            st.stop()

        st.success("✅ Dataset uploaded successfully")

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # -----------------------------
    # PREVIEW DATA
    # -----------------------------
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Info")
    col1, col2 = st.columns(2)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    st.subheader("Column Types")
    st.write(df.dtypes)

    # -------------------------------------------------------
    # ✅ NOTE: Step 4 — credit deduction goes here
    # When you add your analysis run button/logic below,
    # call deduct_credit(st.session_state.access_key)
    # just before showing results. We'll wire this in Step 4.
    # -------------------------------------------------------