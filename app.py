import streamlit as st
import pandas as pd

# -----------------------------
# ACCESS CONTROL
# -----------------------------
TOKEN = st.secrets["APP_ACCESS_TOKEN"]

def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("## 🔐 PanelStatX Private Access")
        st.caption("Enter your access key")

        user_token = st.text_input("Access Key", type="password")

        if st.button("Unlock"):
            if user_token == TOKEN:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid access key")

        st.stop()

check_auth()

# -----------------------------
# MAIN APP
# -----------------------------
st.title("📊 PanelStatX MVP")
st.caption("Panel Data Analysis Made Simple")

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload your dataset (CSV format)",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success("Dataset uploaded successfully")

    # -----------------------------
    # PREVIEW DATA
    # -----------------------------
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Info")
    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")

    st.subheader("Column Types")
    st.write(df.dtypes)