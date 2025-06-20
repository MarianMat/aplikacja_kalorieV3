import streamlit as st
import pandas as pd
import datetime
import os

from calories_utils import add_meal_form, display_meals, daily_summary
from barcode_scan import fetch_product_data
from image_ai import estimate_calories_from_image

MEALS_CSV = "meals_data.csv"
USERS_CSV = "users.csv"

# ------------------------ LOGOWANIE ------------------------
def login():
    st.title("🍽️ Aplikacja Kalorii")
    st.subheader("🔐 Zaloguj się")

    username = st.text_input("Login")
    password = st.text_input("Hasło", type="password")

    if st.button("Zaloguj"):
        if username == "demo" and password == "demo":
            st.session_state["username"] = username
            if "demo_login_time" not in st.session_state:
                st.session_state["demo_login_time"] = datetime.datetime.now()
            st.experimental_rerun()
        else:
            try:
                users = pd.read_csv(USERS_CSV)
                user = users[(users["username"] == username) & (users["password"] == password)]
                if not user.empty and user.iloc[0]["is_active"]:
                    st.session_state["username"] = username
                    st.experimental_rerun()
                else:
                    st.error("Nieprawidłowe dane logowania lub konto nieaktywne.")
            except FileNotFoundError:
                st.error("Brak bazy użytkowników.")

# ------------------------ BLOKADA DOSTĘPU DEMO ------------------------
def check_demo_access():
    if st.session_state.get("username") == "demo":
        now = datetime.datetime.now()
        first_login = st.session_state.get("demo_login_time")
        if first_login and (now - first_login > datetime.timedelta(days=1)):
            st.warning("Twoja sesja demo wygasła. Skontaktuj się z właścicielem aplikacji.")
            return False
    return True

# ------------------------ GŁÓWNA APLIKACJA ------------------------
def main():
    st.sidebar.title("📌 Menu")
    st.sidebar.write(f"👤 Zalogowany jako: `{st.session_state['username']}`")

    if st.sidebar.button("🚪 Wyloguj się"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

    st.sidebar.subheader("📈 Wykres kalorii")
    try:
        df = pd.read_csv(MEALS_CSV)
        df_user = df[df["username"] == st.session_state["username"]]

        if not df_user.empty:
            df_user["date"] = pd.to_datetime(df_user["date"]).dt.date
            summary = df_user.groupby("date")["calories"].sum().reset_index()

            import matplotlib.pyplot as plt
            import seaborn as sns

            fig, ax = plt.subplots()
            sns.barplot(data=summary, x="date", y="calories", ax=ax)
            ax.set_title("Kalorie dziennie")
            ax.set_xlabel("Data")
            ax.set_ylabel("Kalorie")
            plt.xticks(rotation=45)
            st.sidebar.pyplot(fig)
        else:
            st.sidebar.info("Brak danych do wykresu.")
    except FileNotFoundError:
        st.sidebar.info("Brak danych do wykresu.")

    st.sidebar.subheader("📥 Pobierz dane")
    if os.path.exists(MEALS_CSV):
        df = pd.read_csv(MEALS_CSV)
        df_user = df[df["username"] == st.session_state["username"]]
        csv = df_user.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button("⬇️ Pobierz CSV", data=csv, file_name="posilki.csv", mime="text/csv")

    st.title("🍽️ Twój dziennik kalorii")
    st.markdown("---")

    if check_demo_access():
        add_meal_form(st.session_state["username"])

        try:
            df = pd.read_csv(MEALS_CSV)
            df = df[df["username"] == st.session_state["username"]]
        except FileNotFoundError:
            df = pd.DataFrame()

        if not df.empty:
            display_meals(df)
            daily_summary(df)

# ------------------------ START ------------------------
if "username" not in st.session_state:
    login()
else:
    main()
