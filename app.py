import streamlit as st
from auth import check_login, load_user_data
from calories_utils import add_meal_form, display_meals, daily_summary
from stats import show_stats

st.set_page_config(page_title="Liczenie Kalorii", layout="centered")
st.title("🍽️ Licznik Kalorii i IG")

# Informacja o koncie demo
st.info(
    "ℹ️ Możesz zalogować się na konto DEMO:\n\n"
    "- login: **demo**\n"
    "- hasło: **demo**\n\n"
    "Konto demo jest aktywne przez 1 dzień, po czym będzie wymagało kontaktu z właścicielem aplikacji."
)

user = check_login()
if not user:
    st.stop()

user_data = load_user_data(user)

menu = st.sidebar.radio("Menu", ["📅 Dziennik", "📊 Statystyki", "⬇️ Eksport"])

if menu == "📅 Dziennik":
    daily_summary(user_data)
    add_meal_form(user)
    display_meals(user_data)

elif menu == "📊 Statystyki":
    show_stats(user)

elif menu == "⬇️ Eksport":
    st.download_button(
        "Pobierz dane jako CSV",
        data=user_data.to_csv(index=False),
        file_name=f"{user}_dane.csv"
    )
