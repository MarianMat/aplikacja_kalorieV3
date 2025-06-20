import streamlit as st
import hashlib
import datetime

# Słownik użytkowników z hasłami i datą wygaśnięcia
USERS = {
    "demo": {
        "password_hash": hashlib.sha256("demo".encode()).hexdigest(),
        "active": True,
        "expire_date": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")  # demo ważne 1 dzień
    },
    "Wolf": {
        "password_hash": hashlib.sha256("Wolf".encode()).hexdigest(),
        "active": True,
        "expire_date": None  # konto aktywne na zawsze
    }
}

def hash_password(password):
    # Hashuje hasło SHA256
    return hashlib.sha256(password.encode()).hexdigest()

def check_login():
    # Obsługa logowania w Streamlit ze stanem sesji
    if "login" not in st.session_state:
        st.session_state.login = False
        st.session_state.user = None

    if not st.session_state.login:
        st.title("🔐 Logowanie")
        st.info("Konto demo: login 'demo', hasło 'demo'")
        st.info("Konto Wolf: login 'Wolf', hasło 'Wolf'")

        username = st.text_input("Login")
        password = st.text_input("Hasło", type="password")

        if st.button("Zaloguj"):
            if username not in USERS:
                st.error("Niepoprawny login lub hasło.")
                return None

            user = USERS[username]
            if hash_password(password) == user["password_hash"]:
                if not user["active"]:
                    st.error("Konto nieaktywne. Skontaktuj się z administratorem.")
                    return None

                if user["expire_date"]:
                    expire_date = datetime.datetime.strptime(user["expire_date"], "%Y-%m-%d")
                    if expire_date < datetime.datetime.now():
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
        # Jeśli już zalogowany, zwraca nazwę użytkownika
        return st.session_state.user
