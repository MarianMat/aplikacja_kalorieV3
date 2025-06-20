import streamlit as st
import pandas as pd
import hashlib
import datetime

USERS_CSV = "database.csv"
PENDING_CSV = "pending_users.csv"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        df = pd.read_csv(USERS_CSV)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["username", "password_hash", "active", "expire_date"])
    return df

def save_users(df):
    df.to_csv(USERS_CSV, index=False)

def check_login():
    if "login" not in st.session_state:
        st.session_state.login = False
        st.session_state.user = None

    if not st.session_state.login:
        st.title("🔐 Logowanie")

        # ✅ Info o koncie demo – pokazuje się tylko przed zalogowaniem
        st.info("ℹ️ Możesz przetestować aplikację: **login: demo** / **hasło: demo**.\nKonto demo działa przez 1 dzień.")

        username = st.text_input("Login")
        password = st.text_input("Hasło", type="password")

        if st.button("Zaloguj"):
            users = load_users()
            user_row = users[users["username"] == username]
