import streamlit as st
from auth import check_login
from calories_utils import add_meal_form, display_meals, daily_summary

from barcode_scan import fetch_product_data
from image_ai import estimate_calories_from_image

def main():
    user = check_login()
    if not user:
        return

    st.title(f"Witaj, {user}!")

    option = st.radio("Wybierz metodę dodania posiłku:", ["Ręcznie", "Kod kreskowy", "Zdjęcie AI"])

    if option == "Ręcznie":
        add_meal_form(user)

    elif option == "Kod kreskowy":
        barcode = st.text_input("Wpisz kod kreskowy produktu")
        if st.button("Szukaj produktu"):
            if barcode:
                product = fetch_product_data(barcode)
                if product:
                    st.write("Znaleziony produkt:")
                    st.json(product)
                    # Możesz tu dodać możliwość dodania produktu do posiłków, np. formularz z wypełnionymi polami
                else:
                    st.error("Nie znaleziono produktu o takim kodzie.")
            else:
                st.warning("Wpisz kod kreskowy.")

    elif option == "Zdjęcie AI":
        image_file = st.file_uploader("Wgraj zdjęcie posiłku", type=["png", "jpg", "jpeg"])
        camera_image = st.camera_input("Lub zrób zdjęcie kamerą")
        img = image_file or camera_image
        if img:
            st.image(img, caption="Wybrane zdjęcie", use_column_width=True)
            if st.button("Analizuj zdjęcie i szacuj kalorie"):
                result = estimate_calories_from_image(img)
                st.write("Wynik analizy AI:")
                st.markdown(result)

    import pandas as pd
    try:
        df = pd.read_csv("meals_data.csv")
        df = df[df["username"] == user]
    except FileNotFoundError:
        df = pd.DataFrame()

    if not df.empty:
        display_meals(df)
        daily_summary(df)
    else:
        st.info("Nie dodano jeszcze żadnych posiłków.")

if __name__ == "__main__":
    main()
