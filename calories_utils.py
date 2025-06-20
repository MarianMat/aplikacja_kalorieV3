import streamlit as st
import pandas as pd
import datetime

MEALS_CSV = "meals_data.csv"

def add_meal_form(username):
    # Formularz do ręcznego dodawania posiłku
    with st.form("Dodaj posiłek"):
        st.subheader("➕ Dodaj posiłek")

        meal_name = st.text_input("Nazwa produktu")
        weight = st.number_input("Waga (g)", min_value=0)
        calories = st.number_input("Kalorie (kcal)", min_value=0.0)

        protein = st.number_input("Białko (g) na 100g", value=0.0, min_value=0.0)
        carbs = st.number_input("Węglowodany (g) na 100g", value=0.0, min_value=0.0)
        fat = st.number_input("Tłuszcze (g) na 100g", value=0.0, min_value=0.0)

        meal_type = st.selectbox("Typ posiłku", ["śniadanie", "obiad", "kolacja", "przekąska", "inne"])
        date = st.date_input("Data", value=datetime.date.today())
        time = st.time_input("Godzina", value=datetime.datetime.now().time())

        glycemic_index = st.number_input("Indeks glikemiczny", min_value=0)

        submitted = st.form_submit_button("Zapisz posiłek")

        if submitted and meal_name and weight > 0 and calories > 0:
            new_data = {
                "username": username,
                "date": pd.to_datetime(f"{date} {time}"),
                "meal_name": meal_name,
                "weight": weight,
                "calories": calories,
                "protein": protein,
                "carbs": carbs,
                "fat": fat,
                "meal_type": meal_type,
                "glycemic_index": glycemic_index
            }

            try:
                df = pd.read_csv(MEALS_CSV)
            except FileNotFoundError:
                df = pd.DataFrame(columns=new_data.keys())

            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(MEALS_CSV, index=False)
            st.success("✅ Posiłek zapisany.")
        elif submitted:
            st.error("❗ Uzupełnij wszystkie pola.")

def display_meals(df):
    # Wyświetla listę posiłków dla aktualnego dnia
    st.subheader("📋 Lista posiłków (dzisiaj)")
    today = pd.Timestamp(datetime.date.today())
    day_meals = df[pd.to_datetime(df["date"]).dt.date == today.date()]

    if day_meals.empty:
        st.info("Brak zapisanych posiłków na dziś.")
    else:
        st.dataframe(day_meals[["date", "meal_name", "weight", "calories", "protein", "carbs", "fat", "meal_type", "glycemic_index"]])

def daily_summary(df):
    # Podsumowanie kaloryczne i makroskładniki dnia
    st.subheader("📊 Podsumowanie dzienne")

    today = pd.Timestamp(datetime.date.today())
    today_meals = df[pd.to_datetime(df["date"]).dt.date == today.date()]

    if today_meals.empty:
        st.info("Brak danych do podsumowania.")
        return

    total_calories = today_meals["calories"].sum()
    total_protein = today_meals["protein"].sum()
    total_carbs = today_meals["carbs"].sum()
    total_fat = today_meals["fat"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Kalorie", f"{total_calories:.0f} kcal")
    col2.metric("Białko", f"{total_protein:.1f} g")
    col3.metric("Węglowodany", f"{total_carbs:.1f} g")
    col4.metric("Tłuszcz", f"{total_fat:.1f} g")

