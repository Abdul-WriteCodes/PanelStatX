import streamlit as st
import pandas as pd



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
    """,
    unsafe_allow_html=True
)
st.markdown("---")

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

# ---------------- HEADER ----------------
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
    """,
    unsafe_allow_html=True
)
st.markdown("---")






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

        st.success("Dataset uploaded successfully")

        # Preview
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

    except Exception as e:
        st.error(f"Error reading file: {e}")


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