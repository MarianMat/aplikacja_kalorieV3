import openai
import streamlit as st
from io import BytesIO

# Pobierz klucz API z sekretów Streamlit
openai.api_key = st.secrets["OPENAI_API_KEY"]

def estimate_calories_from_image(image_file):
    """
    Wysyła zdjęcie do OpenAI GPT-4o-mini z wizją i zwraca szacunkowe wartości odżywcze.

    image_file: plik obrazu (BytesIO lub podobny) - np. st.file_uploader() lub st.camera_input()
    """

    # Wczytujemy obraz jako bajty
    image_bytes = image_file.read()

    try:
        # Wywołanie API z funkcją wizji (multi-modal)
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            modalities=["text", "image"],
            messages=[
                {"role": "system", "content": "Jesteś ekspertem dietetykiem, który szacuje kalorie i makroskładniki na podstawie zdjęcia posiłku."},
                {"role": "user", "content": "Na podstawie tego zdjęcia podaj przybliżoną wartość kalorii, białka, tłuszczu i węglowodanów w gramach."}
            ],
            images=[{"image": image_bytes}],
            temperature=0.3
        )
        # Odczyt odpowiedzi tekstowej
        text_response = response.choices[0].message.content

        # Przykładowo parsujemy odpowiedź - zakładamy, że AI zwróci np. tekst w formacie JSON lub prostym
        # Możesz dopasować parser do formatu, który zwraca AI.
        # Tutaj na potrzeby demo zwrócimy surowy tekst.
        return text_response

    except Exception as e:
        return f"Błąd podczas przetwarzania obrazu: {e}"
