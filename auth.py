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

            if user_row.empty:
                st.error("Niepoprawny login lub hasło.")
                return None

            user_data = user_row.iloc[0]
            if hash_password(password) == user_data["password_hash"]:
                # Konto Chmarynka (Wolf) – zawsze aktywne
                if username == "Wolf":
                    st.session_state.login = True
                    st.session_state.user = username
                    st.success(f"🌥️ Zalogowano jako Chmarynka")
                    return username

                # Sprawdzenie aktywności konta
                if not user_data["active"]:
                    st.error("⛔ Konto nieaktywne. Skontaktuj się z administratorem.")
                    return None

                # Sprawdzenie daty ważności konta
                if pd.notna(user_data["expire_date"]):
                    expire_date = pd.to_datetime(user_data["expire_date"])
                    if expire_date < pd.Timestamp(datetime.datetime.now()):
                        st.error("⛔ Twoje konto wygasło. Skontaktuj się z administratorem.")
                        return None

                # Konto demo – jeśli wygasło
                if username == "demo" and pd.notna(user_data["expire_date"]):
                    expire_date = pd.to_datetime(user_data["expire_date"])
                    if expire_date < pd.Timestamp(datetime.datetime.now()):
                        st.warning("⛔ Konto demo wygasło. Skontaktuj się z administratorem aby uzyskać dostęp.")
                        return None

                st.session_state.login = True
                st.session_state.user = username
                st.success(f"✅ Zalogowano jako {username}")
                return username
            else:
                st.error("Niepoprawny login lub hasło.")
                return None
        else:
            st.info("Wprowadź dane i kliknij 'Zaloguj'.")
            return None
    else:
        return st.session_state.user

def load_user_data(username):
    try:
        df = pd.read_csv("meals_data.csv")
        user_meals = df[df["username"] == username].copy()
    except FileNotFoundError:
        user_meals = pd.DataFrame(columns=[
            "username", "date", "meal_name", "weight", "calories",
            "protein", "carbs", "fat", "meal_type", "glycemic_index"
        ])
    return user_meals

