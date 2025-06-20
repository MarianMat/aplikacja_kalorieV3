import streamlit as st
import hashlib
import datetime

# Użytkownicy
USERS = {
    "demo": {
        "password_hash": hashlib.sha256("demo".encode()).hexdigest(),
        "active": True,
        "expire_date": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    },
    "Wolf": {
        "password_hash": hashlib.sha256("Wolf".encode()).hexdigest(),
        "active": True,
        "expire_date": None
    }
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login():
    if "login" not in st.session_state:
        st.session_state.login = False
        st.session_state.user = None

    if not st.session_state.login:
        st.title("🔐 Logowanie")
        st.info("Konto demo: login `demo`, hasło `demo`")

        username = st.text_input("Login")
        password = st.text_input("Hasło", type="password")

        if st.button("Zaloguj"):
            if username not in USERS:
                st.error("Niepoprawny login lub hasło.")
                return None

            user = USERS[username]
            if hash_password(password) == user["password_hash"]:
                if not user["active"]:
                    st.error("Konto nieaktywne.")
                    return None

                if user["expire_date"]:
                    if datetime.datetime.strptime(user["expire_date"], "%Y-%m-%d") < datetime.datetime.now():
                        st.error("Twoje konto wygasło.")
                        return None

                st.session_state.login = True
                st.session_state.user = username
                st.success(f"Zalogowano jako {username}")
                return username
            else:
                st.error("Niepoprawny login lub hasło.")
                return None
    else:
        return st.session_state.user
