import streamlit as st
from auth import check_login, load_user_data
from calories_utils import add_meal_form, display_meals, daily_summary, glycemic_index_alert
from barcode_scan import barcode_input_form
from image_ai import image_upload_form

def main():
    user = check_login()

    if user:
        st.title(f"Witaj, {user}!")

        # Informacja o koncie demo tylko raz
        if user == "demo" and "demo_info_shown" not in st.session_state:
            st.info("Używasz konta DEMO (login: demo, hasło: demo). Konto jest aktywne 1 dzień.")
            st.session_state.demo_info_shown = True

        st.markdown("---")
        st.header("📦 Wprowadź lub zeskanuj kod kreskowy produktu")
        product_data = barcode_input_form()

        st.markdown("---")
        st.header("📷 Rozpoznawanie kalorii ze zdjęcia posiłku")
        calories_from_image = image_upload_form()

        st.markdown("---")
        st.header("➕ Dodaj posiłek ręcznie")
        add_meal_form(user)

        st.markdown("---")
        df = load_user_data(user)
        display_meals(df)
        daily_summary(df)

        # Pokaz alert indeksu glikemicznego dla ostatniego posiłku
        if not df.empty and "glycemic_index" in df.columns:
            latest_gi = df.iloc[-1]["glycemic_index"]
            glycemic_index_alert(latest_gi)

if __name__ == "__main__":
    main()
