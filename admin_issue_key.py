"""
PanelStatX — Admin Key Issuer
─────────────────────────────
Run this locally to issue a new access key after a Flutterwave payment is confirmed.

Usage:
    python admin_issue_key.py

Requirements:
    pip install gspread google-auth

Expects a  secrets.json  file in the same directory (your service-account JSON key),
OR set the env var  GOOGLE_APPLICATION_CREDENTIALS  to point to it.

Edit the SHEET_ID constant below before first use.
"""

import json
import sys
import uuid
import datetime
import gspread
from google.oauth2.service_account import Credentials

# ── Config ────────────────────────────────────────────────────────────────────
SHEET_ID    = "1PeZ1FDhfKwEzQ-Kervm_wOn58dfmQ0RLhc8z60I_kTQ"   # ← change this
CREDS_FILE  = "panelstatx-271958e2a874.json"   # path to your service-account JSON key
SCOPES      = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# ── Key generation ────────────────────────────────────────────────────────────
def generate_key() -> str:
    """Produce a human-readable key like PSX-A1B2-C3D4-E5F6."""
    raw = uuid.uuid4().hex.upper()
    return f"PSX-{raw[0:4]}-{raw[4:8]}-{raw[8:12]}"


# ── Sheet helpers ─────────────────────────────────────────────────────────────
def get_worksheet():
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    gc    = gspread.authorize(creds)
    sh    = gc.open_by_key(SHEET_ID)
    ws    = sh.sheet1

    # Ensure header row exists
    existing = ws.row_values(1)
    if not existing or existing[0].strip().lower() != "key":
        ws.insert_row(["Key", "Credits", "DatePurchased", "Email"], index=1)
        print("✓ Header row created.")
    return ws


def key_exists(ws, key: str) -> bool:
    keys = ws.col_values(1)   # column A
    return key in keys


def issue_key(ws, key: str, credits: int, email: str) -> None:
    date_str = datetime.date.today().isoformat()
    ws.append_row([key, credits, date_str, email])
    print(f"\n✅ Key issued successfully!")
    print(f"   Key            : {key}")
    print(f"   Credits        : {credits}")
    print(f"   Date purchased : {date_str}")
    print(f"   Email          : {email}")


def topup_key(ws, key: str, add_credits: int) -> None:
    """Add credits to an existing key."""
    keys = ws.col_values(1)
    try:
        row_idx = keys.index(key) + 1   # gspread is 1-indexed
    except ValueError:
        print(f"❌ Key not found: {key}")
        return

    current = int(ws.cell(row_idx, 2).value or 0)
    new_val  = current + add_credits
    ws.update_cell(row_idx, 2, new_val)
    print(f"\n✅ Top-up successful!")
    print(f"   Key      : {key}")
    print(f"   Previous : {current}  →  New: {new_val}")


def list_keys(ws) -> None:
    records = ws.get_all_records()
    if not records:
        print("No keys in sheet yet.")
        return
    print(f"\n{'Key':<22} {'Credits':>8}  {'Date':<14}  Email")
    print("─" * 70)
    for r in records:
        flag = "⚠ " if int(r.get("Credits", 0)) <= 0 else "   "
        print(f"{flag}{r['Key']:<20} {r['Credits']:>8}  {r['DatePurchased']:<14}  {r['Email']}")


# ── CLI menu ──────────────────────────────────────────────────────────────────
def main():
    print("\n⬡  PanelStatX — Admin Key Manager")
    print("=" * 40)
    print("1. Issue new key")
    print("2. Top-up existing key")
    print("3. List all keys")
    print("4. Exit")
    choice = input("\nChoice [1-4]: ").strip()

    ws = get_worksheet()

    if choice == "1":
        email   = input("User email         : ").strip()
        credits = input("Credits to grant   [default 10]: ").strip()
        credits = int(credits) if credits.isdigit() else 10
        key     = generate_key()

        # Guarantee uniqueness
        while key_exists(ws, key):
            key = generate_key()

        issue_key(ws, key, credits, email)
        print(f"\n   → Send this key to the user: {key}\n")

    elif choice == "2":
        key     = input("Existing key  : ").strip()
        add     = input("Credits to add [default 10]: ").strip()
        add     = int(add) if add.isdigit() else 10
        topup_key(ws, key, add)

    elif choice == "3":
        list_keys(ws)

    elif choice == "4":
        sys.exit(0)

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
