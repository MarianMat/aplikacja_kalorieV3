import datetime
import streamlit as st

# Prosta baza użytkowników i haseł (na potrzeby demo, bez hashowania)
USERS = {
    "demo": "demo",
    "Wolf": "Wolf",
}

# Czas ważności konta demo (w godzinach)
DEMO_EXPIRATION_HOURS = 24

def check_login(username: str, password: str) -> bool:
    username = username.strip()
    password = password.strip()

    if username not in USERS:
        return False

    if USERS[username] != password:
        return False

    # Konto Wolf jest zawsze aktywne
    if username == "Wolf":
        return True

    # Konto demo jest ważne tylko 24 godziny od zalogowania
    if username == "demo":
        # Sprawdzamy czy w sesji mamy czas logowania
        login_time = st.session_state.get("login_time", None)
        if login_time is None:
            # Jeśli nie ma, to logowanie jest OK (pierwsze logowanie)
            return True
        else:
            now = datetime.datetime.now()
            if isinstance(login_time, str):
                # Jeśli login_time zapisał się jako string, konwertujemy
                try:
                    login_time = datetime.datetime.fromisoformat(login_time)
                except Exception:
                    return False
            elapsed = now - login_time
            if elapsed.total_seconds() > DEMO_EXPIRATION_HOURS * 3600:
                # Przekroczono 24h - demo wygasło
                return False
            else:
                return True

    # Inne konta (jeśli dodasz) — domyślnie odrzucamy
    return False

def get_display_name(username: str) -> str:
    if username == "Wolf":
        return "Chmarynka 😶‍🌫️"
    return username
