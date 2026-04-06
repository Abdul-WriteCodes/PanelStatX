import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


@st.cache_resource
def get_sheet():
    """Authenticate and return the worksheet."""
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(st.secrets["SHEET_ID"])
    return sheet.sheet1  # First sheet tab


def get_all_keys():
    """Return all rows as list of dicts."""
    ws = get_sheet()
    return ws.get_all_records()


def find_key_row(access_key: str):
    """
    Find the row number and data for a given access key.
    Returns (row_index, row_data) or (None, None) if not found.
    Row index is 1-based, accounting for header row.
    """
    ws = get_sheet()
    records = ws.get_all_records()

    for i, row in enumerate(records):
        if str(row["access_key"]).strip() == access_key.strip():
            return i + 2, row  # +2: row 1 is header, enumerate starts at 0

    return None, None


def deduct_credit(access_key: str):
    """
    Subtract 1 credit from the key's row.
    Blocks the key automatically if credits reach 0.
    Returns updated credit count, or None if key not found.
    """
    ws = get_sheet()
    row_num, row_data = find_key_row(access_key)

    if row_num is None:
        return None

    new_credits = int(row_data["credits"]) - 1

    # Update credits column (column B = 2)
    ws.update_cell(row_num, 2, new_credits)

    # Auto-block key if credits exhausted
    if new_credits <= 0:
        ws.update_cell(row_num, 4, "blocked")  # column D = status

    return new_credits