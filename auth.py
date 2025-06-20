import streamlit as st
import pandas as pd
import hashlib
import datetime
import os

USERS_CSV = "database.csv"
PENDING_CSV = "pending_users.csv"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login():
    if "login" not in st.session_state:
        st.session_state.login = False
        st.session_state.user = None

    if not st.session_state.login:
        st.title("🔐 Logowanie")

        # 👇 Jednorazowa informacja o demo przed zalogowaniem
        st.info("ℹ️ Możesz przetestować aplikację: **login: demo** / **hasło: demo**. Konto demo działa tylko przez 1 dzień.")

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
                if not user_data["active"]:
                    st.error("Konto nieaktywne. Skontaktuj się z administratorem.")
                    return None
                if pd.notna(user_data["expire_date"]):
                    expire_date = pd.to_datetime(user_data["expire_date"])
                    if expire_date < pd.Timestamp(datetime.datetime.now()):
                        st.error("Twoje konto wygasło. Skontaktuj się z administratorem.")
                        return None
                if username == "demo" and pd.notna(user_data["expire_date"]):
                    expire_date = pd.to_datetime(user_data["expire_date"])
                    if expire_date < pd.Timestamp(datetime.datetime.now()):
                        st.warning("⛔ Demo wygasło. Skontaktuj się z administratorem aby uzyskać pełne konto.")
                        return None

                st.session_state.login = True
                st.session_state.user = username
                st.success(f"Zalogowano jako {username}")
                return username
            else:
                st.error("Niepoprawny login lub hasło.")
                return None
        else:
            st.info("Wprowadź dane i kliknij 'Zaloguj'.")
            return None
    else:
        return st.session_state.user

def load_users():
    try:
        df = pd.read_csv(USERS_CSV)
    except FileNotFoundError:
        create_default_users()
        df = pd.read_csv(USERS_CSV)
    return df

def save_users(df):
    df.to_csv(USERS_CSV, index=False)

def check_login():
    create_default_users()  # upewnij się, że użytkownicy demo i Wolf istnieją
    
    if "login" not in st.session_state:
        st.session_state.login = False
        st.session_state.user = None

    if not st.session_state.login:
        st.title("🔐 Logowanie")

        # Informacja o demo
        st.info(
            "ℹ️ Możesz zalogować się na konto DEMO:\n\n"
            "- login: **demo**\n"
            "- hasło: **demo**\n\n"
            "Konto demo jest aktywne przez 1 dzień, po czym będzie wymagało kontaktu z właścicielem aplikacji."
        )

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
                # Sprawdź ważność konta i demo
                if not user_data["active"]:
                    st.error("Konto nieaktywne. Skontaktuj się z administratorem.")
                    return None
                if pd.notna(user_data["expire_date"]) and user_data["expire_date"] != "":
                    expire_date = pd.to_datetime(user_data["expire_date"])
                    if expire_date < pd.Timestamp(datetime.datetime.now()):
                        if username == "demo":
                            st.warning("Demo wygasło. Skontaktuj się z administratorem, aby uzyskać pełne konto.")
                        else:
                            st.error("Twoje konto wygasło. Skontaktuj się z administratorem.")
                        return None

                st.session_state.login = True
                st.session_state.user = username
                st.success(f"Zalogowano jako {username}")
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
    # Załaduj dane posiłków z pliku CSV (można rozbudować o bazę SQL itp.)
    try:
        df = pd.read_csv("meals_data.csv")
        user_meals = df[df["username"] == username].copy()
    except FileNotFoundError:
        user_meals = pd.DataFrame(columns=["username", "date", "meal_name", "weight", "calories", "protein", "carbs", "fat", "meal_type", "glycemic_index"])

    return user_meals
