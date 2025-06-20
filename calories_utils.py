# Oblicimport streamlit as st
import pandas as pd
import datetime

MEALS_FILE = "meals_data.csv"

# Lista z wartościami IG dla popularnych produktów - możesz rozbudować
GI_LIST = {
    "chleb biały": 70,
    "ryż biały": 73,
    "banan": 51,
    "jabłko": 38,
    "marchew": 35,
    "ziemniaki": 85,
    "makaron": 50,
    # dodaj inne
}

def calculate_gi(meal_name):
    name_lower = meal_name.lower()
    for key in GI_LIST.keys():
        if key in name_lower:
            return GI_LIST[key]
    return None  # jeśli nieznany

def calculate_calories(weight, calories_per_100g):
    return (weight * calories_per_100g) / 100

def add_meal_form(username, prefilled=None):
    with st.form("add_meal_form"):
        if prefilled:
            name_default = prefilled.get("name", "")
            calories_default = prefilled.get("calories", 0)
            protein_default = prefilled.get("protein", 0)
            carbs_default = prefilled.get("carbs", 0)
            fat_default = prefilled.get("fat", 0)
        else:
            name_default = ""
            calories_default = 0
            protein_default = 0
            carbs_default = 0
            fat_default = 0

        meal_name = st.text_input("Nazwa produktu", value=name_default)
        weight = st.number_input("Waga/ilość (g)", min_value=1, step=1)
        calories_per_100g = st.number_input("Kalorie na 100g", value=calories_default, min_value=0)
        protein = st.number_input("Białko (g) na 100g", value=protein_default, min_value=0.0)
        carbs = st.number_input("Węglowodany (g) na 100g", value=carbs_default, min_value=0.0)
        fat = st.number_input("Tłuszcz (g) na 100g", value=fat_default, min_value=0.0)
        meal_type = st.selectbox("Typ posiłku", ["śniadanie", "obiad", "kolacja", "przekąska", "inne"])
        date = st.date_input("Data posiłku", value=datetime.date.today())
        time = st.time_input("Godzina posiłku", value=datetime.datetime.now().time())

        submitted = st.form_submit_button("Dodaj posiłek")

        if submitted:
            calories = calculate_calories(weight, calories_per_100g)
            gi = calculate_gi(meal_name)
            new_entry = {
                "username": username,
                "date": f"{date} {time.strftime('%H:%M')}",
                "meal_name": meal_name,
                "weight": weight,
                "calories": calories,
                "protein": protein,
                "carbs": carbs,
                "fat": fat,
                "meal_type": meal_type,
                "glycemic_index": gi if gi else -1
            }

            try:
                df = pd.read_csv(MEALS_FILE)
            except FileNotFoundError:
                df = pd.DataFrame(columns=new_entry.keys())

            df = df
zenia kalorii i indeks glikemiczny
