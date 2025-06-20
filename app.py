# Folder: aplikacja_kalorie/

# --- app.py ---
# Główny plik aplikacji Streamlit
import streamlit as st
from auth import check_login, load_user_data
from calories_utils import add_meal_form, display_meals, daily_summary
from stats import show_stats

st.set_page_config(page_title="Liczenie Kalorii", layout="centered")
st.title("🍽️ Licznik Kalorii i IG")

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
    st.download_button("Pobierz dane jako CSV", data=user_data.to_csv(index=False), file_name=f"{user}_dane.csv")
