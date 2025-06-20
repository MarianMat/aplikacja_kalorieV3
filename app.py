import streamlit as st
from auth import check_login, load_user_data
from calories_utils import add_meal_form, display_meals, daily_summary
from stats import show_stats
from barcode_scan import scan_barcode_and_get_data
from image_ai import analyze_image_calories

st.set_page_config(page_title="Liczenie Kalorii i IG", layout="centered")

st.title("🍽️ Licznik Kalorii i Indeksu Glikemicznego")

user = check_login()
if not user:
    st.stop()

user_data = load_user_data(user)

menu = st.sidebar.radio("Menu", ["📅 Dziennik", "📊 Statystyki", "⬇️ Eksport"])

if menu == "📅 Dziennik":
    daily_summary(user_data)

    st.markdown("---")
    st.subheader("Dodaj nowy posiłek")

    option = st.radio("Wybierz metodę dodania posiłku:", ["Ręczne dodanie", "Skanuj kod kreskowy", "Analiza zdjęcia"])

    if option == "Ręczne dodanie":
        add_meal_form(user)

    elif option == "Skanuj kod kreskowy":
        barcode = st.text_input("Wpisz lub zeskanuj kod kreskowy (EAN):")
        if barcode:
            product_info = scan_barcode_and_get_data(barcode)
            if product_info:
                st.write(f"Nazwa: {product_info['name']}")
                st.write(f"Kalorie na 100g: {product_info['calories']} kcal")
                add_meal_form(user, prefilled=product_info)
            else:
                st.error("Nie znaleziono produktu w bazie OpenFoodFacts.")

    elif option == "Analiza zdjęcia":
        uploaded_file = st.file_uploader("Prześlij zdjęcie posiłku", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            with st.spinner("Analizuję zdjęcie..."):
                result = analyze_image_calories(uploaded_file)
                if result:
                    st.write(f"Szacowane kalorie: {result['calories']} kcal")
                    add_meal_form(user, prefilled=result)
                else:
                    st.error("Nie udało się rozpoznać kalorii ze zdjęcia.")

    st.markdown("---")
    st.subheader("Twoje posiłki")
    display_meals(user_data)

elif menu == "📊 Statystyki":
    show_stats(user_data)

elif menu == "⬇️ Eksport":
    csv_data = user_data.to_csv(index=False)
    st.download_button("Pobierz dane jako CSV", data=csv_data, file_name=f"{user}_dane.csv")
