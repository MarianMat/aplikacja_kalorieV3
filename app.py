import streamlit as st
from auth import check_login
from calories_utils import add_meal_form, display_meals, daily_summary
from barcode_scan import fetch_product_data
from image_ai import estimate_calories_from_image
import pandas as pd
import datetime
from datetime import date, timedelta
import os

st.set_page_config(page_title="Licznik kalorii", layout="wide")

MEALS_CSV = "meals_data.csv"

# 🧾 PANEL LOGOWANIA
if "username" not in st.session_state:
    st.title("🍽️ Licznik kalorii")

    st.info("ℹ️ Możesz przetestować aplikację używając konta **DEMO**:\n\n**Login:** `demo`  \n**Hasło:** `demo`\n\nDziała tylko przez 24h.")

    username = st.text_input("Login")
    password = st.text_input("Hasło", type="password")
    if st.button("Zaloguj się"):
        if check_login(username, password):
            st.session_state.username = username
            st.session_state.login_time = datetime.datetime.now()
            st.rerun()
        else:
            st.error("Nieprawidłowy login lub hasło.")
    st.stop()

# 📤 PANEL BOCZNY
with st.sidebar:
    st.title("👤 Użytkownik")

    # Wyświetlanie przyjaznej nazwy użytkownika
    username = st.session_state.get("username", "")
    display_name = "Chmarynka ☁️" if username == "Wolf" else username
    st.write(f"Zalogowany jako: **{display_name}**")

    if st.button("🚪 Wyloguj się"):
        st.session_state.clear()
        st.experimental_rerun()

    st.markdown("---")
    st.subheader("📊 Statystyki")
    try:
        df = pd.read_csv(MEALS_CSV)
        user_df = df[df["username"] == st.session_state.username]
    except FileNotFoundError:
        user_df = pd.DataFrame()

    if not user_df.empty:
        # 🔽 Eksport całości
        if st.button("📥 Pobierz wszystkie dane jako CSV"):
            st.download_button(
                label="📥 Pobierz dane jako CSV",
                data=user_df.to_csv(index=False).encode("utf-8"),
                file_name="posilki.csv",
                mime="text/csv"
            )

        # 📈 Wykres z ostatnich 7 dni
        if st.checkbox("📈 Pokaż wykres kalorii z ostatnich 7 dni"):
            last_7 = user_df.copy()
            last_7["date"] = pd.to_datetime(last_7["date"]).dt.date
            chart_df = last_7.groupby("date")["calories"].sum().reset_index()
            st.line_chart(chart_df, x="date", y="calories")

        # 🔍 Nowy zakres dat i eksport danych
        st.markdown("### 📅 Zakres analiz")
        start_date = st.date_input("Od", value=date.today() - timedelta(days=7))
        end_date = st.date_input("Do", value=date.today())

        filtered_df = user_df.copy()
        filtered_df["date"] = pd.to_datetime(filtered_df["date"]).dt.date
        filtered_df = filtered_df[(filtered_df["date"] >= start_date) & (filtered_df["date"] <= end_date)]

        if not filtered_df.empty:
            st.line_chart(filtered_df.groupby("date")["calories"].sum(), use_container_width=True)
            st.write(f"🔢 **Suma kalorii od {start_date} do {end_date}:** {filtered_df['calories'].sum():.0f} kcal")

            export_format = st.radio("Eksportuj dane jako:", ["CSV", "Google Sheets"])
            if st.button("📤 Eksportuj dane"):
                if export_format == "CSV":
                    st.download_button(
                        label="📥 Pobierz CSV",
                        data=filtered_df.to_csv(index=False).encode("utf-8"),
                        file_name=f"kalorie_{start_date}_do_{end_date}.csv",
                        mime="text/csv"
                    )
                elif export_format == "Google Sheets":
                    st.warning("🔒 Eksport do Google Sheets wymaga integracji z Google API (do wdrożenia osobno).")
        else:
            st.info("Brak danych w wybranym zakresie.")

# 🧾 FORMULARZ DODAWANIA POSIŁKU
st.title("➕ Dodaj posiłek")
option = st.radio("Wybierz metodę dodania posiłku:", ["Ręcznie", "Kod kreskowy", "Zdjęcie AI"])

if option == "Ręcznie":
    add_meal_form(st.session_state.username)

elif option == "Kod kreskowy":
    barcode = st.text_input("Wpisz kod kreskowy")
    if st.button("🔍 Pobierz dane z OpenFoodFacts") and barcode:
        data = fetch_product_data(barcode)
        if data:
            st.success("✅ Produkt znaleziony!")
            st.json(data)
            st.session_state.prefill = data
            add_meal_form(st.session_state.username)
        else:
            st.warning("❗ Nie znaleziono produktu.")

elif option == "Zdjęcie AI":
    image_file = st.file_uploader("📷 Wgraj zdjęcie posiłku", type=["jpg", "jpeg", "png"])
    camera_image = st.camera_input("Lub zrób zdjęcie kamerą")

    img = image_file or camera_image

    if img:
        st.image(img, caption="📸 Podgląd zdjęcia", use_column_width=True)
        if st.button("🤖 Analizuj zdjęcie AI"):
            result = estimate_calories_from_image(img)
            st.write("📊 Wynik analizy AI:")
            st.json(result)
            st.session_state.prefill = result
            add_meal_form(st.session_state.username)

# 📋 WYŚWIETLANIE I PODSUMOWANIE
if not user_df.empty:
    display_meals(user_df)
    daily_summary(user_df)
else:
    st.info("Brak zapisanych posiłków.")
