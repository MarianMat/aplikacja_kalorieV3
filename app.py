import streamlit as st
from auth import check_login
from calories_utils import add_meal_form, display_meals, daily_summary
from barcode_scan import fetch_product_data
from image_ai import estimate_calories_from_image
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Licznik kalorii", layout="wide")

MEALS_CSV = "meals_data.csv"

# 🧾 INFORMACJA DLA NIEZALOGOWANYCH
if "username" not in st.session_state:
    st.title("🍽️ Licznik kalorii")

    st.info("ℹ️ Możesz przetestować aplikację używając konta **DEMO**:\n\n**Login:** `demo`  \n**Hasło:** `demo`\n\nDziała tylko przez 24h.")

    username = st.text_input("Login")
    password = st.text_input("Hasło", type="password")
    if st.button("Zaloguj się"):
        if check_login(username, password):
            st.session_state.username = username
            st.session_state.login_time = datetime.datetime.now().isoformat()
            st.rerun()
        else:
            st.error("Nieprawidłowy login lub hasło.")
    st.stop()

# 📤 PANEL BOCZNY
with st.sidebar:
    st.title("👤 Użytkownik")
    st.write(f"Zalogowany jako: **{st.session_state.username}**")
    if st.button("🚪 Wyloguj się"):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.subheader("📊 Statystyki")
    try:
        df = pd.read_csv(MEALS_CSV)
        user_df = df[df["username"] == st.session_state.username]
    except FileNotFoundError:
        user_df = pd.DataFrame()

    if not user_df.empty:
        st.download_button(
            label="📥 Pobierz wszystkie dane jako CSV",
            data=user_df.to_csv(index=False).encode("utf-8"),
            file_name="posilki.csv",
            mime="text/csv"
        )

        if st.checkbox("📈 Pokaż wykres kalorii z ostatnich 7 dni"):
            last_7 = user_df.copy()
            last_7["date"] = pd.to_datetime(last_7["date"]).dt.date
            chart_df = last_7.groupby("date")["calories"].sum().reset_index()
            st.line_chart(chart_df, x="date", y="calories")

        # 📊 PANEL ANALIZY OKRESOWEJ
        st.markdown("---")
        st.subheader("📅 Analiza kalorii w wybranym okresie")

        start_date = st.date_input("Data początkowa", datetime.date.today() - datetime.timedelta(days=7))
        end_date = st.date_input("Data końcowa", datetime.date.today())

        if start_date > end_date:
            st.error("❌ Data początkowa musi być przed końcową.")
        else:
            filtered_df = user_df[
                (pd.to_datetime(user_df["date"]).dt.date >= start_date) &
                (pd.to_datetime(user_df["date"]).dt.date <= end_date)
            ]

            if not filtered_df.empty:
                st.success(f"📈 Znaleziono {len(filtered_df)} posiłków w tym okresie")

                calories_by_day = filtered_df.groupby("date")["calories"].sum().reset_index()

                chart_type = st.selectbox("Typ wykresu", ["Liniowy", "Słupkowy"])
                if chart_type == "Liniowy":
                    st.line_chart(calories_by_day, x="date", y="calories")
                else:
                    st.bar_chart(calories_by_day.set_index("date"))

                st.markdown(f"**🔢 Suma kalorii:** {filtered_df['calories'].sum()} kcal")
                st.markdown(f"**📊 Średnia dzienna:** {filtered_df['calories'].mean():.2f} kcal")

                st.download_button(
                    label="📥 Pobierz CSV z tego okresu",
                    data=filtered_df.to_csv(index=False).encode("utf-8"),
                    file_name=f"posilki_{start_date}_{end_date}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("⚠️ Brak danych w wybranym zakresie.")

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
if 'user_df' in locals() and not user_df.empty:
    display_meals(user_df)
    daily_summary(user_df)
else:
    st.info("Brak zapisanych posiłków.")

