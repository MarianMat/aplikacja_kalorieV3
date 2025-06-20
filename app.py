import streamlit as st
import pandas as pd
import datetime
from barcode_scan import fetch_product_data
from image_ai import estimate_calories_from_image

MEALS_CSV = "meals_data.csv"

def save_meal(username, meal_name, weight, calories, protein, carbs, fat, glycemic_index, meal_type, date, time):
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

def add_meal_form(username):
    st.subheader("➕ Dodaj posiłek")

    method = st.radio("Wybierz sposób dodania posiłku:", 
                      options=["Ręcznie", "Kod kreskowy", "Zdjęcie (AI)"])

    meal_name = ""
    weight = 0
    calories = 0.0
    protein = 0.0
    carbs = 0.0
    fat = 0.0
    glycemic_index = 0
    meal_type = "inne"
    date = datetime.date.today()
    time = datetime.datetime.now().time()

    if method == "Ręcznie":
        with st.form("manual_meal_form"):
            meal_name = st.text_input("Nazwa produktu")
            weight = st.number_input("Waga (g)", min_value=0)
            calories = st.number_input("Kalorie (kcal)", min_value=0.0)
            protein = st.number_input("Białko (g) na 100g", value=0.0, min_value=0.0)
            carbs = st.number_input("Węglowodany (g) na 100g", value=0.0, min_value=0.0)
            fat = st.number_input("Tłuszcze (g) na 100g", value=0.0, min_value=0.0)
            glycemic_index = st.number_input("Indeks glikemiczny", min_value=0)
            meal_type = st.selectbox("Typ posiłku", ["śniadanie", "obiad", "kolacja", "przekąska", "inne"])
            date = st.date_input("Data", value=datetime.date.today())
            time = st.time_input("Godzina", value=datetime.datetime.now().time())
            submitted = st.form_submit_button("Zapisz posiłek")

            if submitted:
                if meal_name and weight > 0 and calories > 0:
                    save_meal(username, meal_name, weight, calories, protein, carbs, fat, glycemic_index, meal_type, date, time)
                    st.success("✅ Posiłek zapisany.")
                else:
                    st.error("❗ Uzupełnij wszystkie pola.")

    elif method == "Kod kreskowy":
        barcode = st.text_input("Wpisz lub zeskanuj kod kreskowy")
        product_data = None
        if barcode:
            product_data = fetch_product_data(barcode)
            if product_data:
                st.success(f"Produkt: {product_data['product_name']}")
                st.write(f"Kalorie: {product_data['calories']} kcal/100g")
                st.write(f"Białko: {product_data['protein']} g/100g")
                st.write(f"Tłuszcze: {product_data['fat']} g/100g")
                st.write(f"Węglowodany: {product_data['carbs']} g/100g")

                with st.form("barcode_meal_form"):
                    meal_name = st.text_input("Nazwa produktu", value=product_data['product_name'])
                    weight = st.number_input("Waga (g)", min_value=0)
                    calories = st.number_input("Kalorie (kcal)", min_value=0.0, value=product_data['calories'])
                    protein = st.number_input("Białko (g) na 100g", value=product_data['protein'], min_value=0.0)
                    carbs = st.number_input("Węglowodany (g) na 100g", value=product_data['carbs'], min_value=0.0)
                    fat = st.number_input("Tłuszcze (g) na 100g", value=product_data['fat'], min_value=0.0)
                    glycemic_index = st.number_input("Indeks glikemiczny", min_value=0)
                    meal_type = st.selectbox("Typ posiłku", ["śniadanie", "obiad", "kolacja", "przekąska", "inne"])
                    date = st.date_input("Data", value=datetime.date.today())
                    time = st.time_input("Godzina", value=datetime.datetime.now().time())
                    submitted = st.form_submit_button("Zapisz posiłek")

                    if submitted:
                        if meal_name and weight > 0 and calories > 0:
                            save_meal(username, meal_name, weight, calories, protein, carbs, fat, glycemic_index, meal_type, date, time)
                            st.success("✅ Posiłek zapisany.")
                        else:
                            st.error("❗ Uzupełnij wszystkie pola.")

            else:
                st.error("Nie znaleziono produktu o podanym kodzie kreskowym.")

    else:  # Zdjęcie AI
        uploaded_file = st.file_uploader("Prześlij zdjęcie posiłku", type=["png", "jpg", "jpeg"])
        calories_from_image = None
        if uploaded_file:
            st.image(uploaded_file, caption="Twoje zdjęcie", use_column_width=True)
            calories_from_image = estimate_calories_from_image(uploaded_file)

        with st.form("image_meal_form"):
            meal_name = st.text_input("Nazwa produktu")
            weight = st.number_input("Waga (g)", min_value=0)
            calories = st.number_input("Kalorie (kcal)", min_value=0.0, value=calories_from_image if calories_from_image else 0.0)
            protein = st.number_input("Białko (g) na 100g", value=0.0, min_value=0.0)
            carbs = st.number_input("Węglowodany (g) na 100g", value=0.0, min_value=0.0)
            fat = st.number_input("Tłuszcze (g) na 100g", value=0.0, min_value=0.0)
            glycemic_index = st.number_input("Indeks glikemiczny", min_value=0)
            meal_type = st.selectbox("Typ posiłku", ["śniadanie", "obiad", "kolacja", "przekąska", "inne"])
            date = st.date_input("Data", value=datetime.date.today())
            time = st.time_input("Godzina", value=datetime.datetime.now().time())
            submitted = st.form_submit_button("Zapisz posiłek")

            if submitted:
                if meal_name and weight > 0 and calories > 0:
                    save_meal(username, meal_name, weight, calories, protein, carbs, fat, glycemic_index, meal_type, date, time)
                    st.success("✅ Posiłek zapisany.")
                else:
                    st.error("❗ Uzupełnij wszystkie pola.")

def main():
    st.title("Aplikacja do liczenia kalorii")

    # Na potrzeby testu - na sztywno:
    username = "demo_user"

    add_meal_form(username)

if __name__ == "__main__":
    main()

