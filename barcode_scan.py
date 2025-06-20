import requests

def fetch_product_data(barcode: str):
    """
    Pobiera dane produktu po kodzie kreskowym z OpenFoodFacts.
    Zwraca słownik z nazwą produktu i wartościami odżywczymi lub None jeśli brak.
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == 1:
            product = data["product"]
            result = {
                "product_name": product.get("product_name", "Brak nazwy"),
                "calories": float(product.get("nutriments", {}).get("energy-kcal_100g", 0)),
                "protein": float(product.get("nutriments", {}).get("proteins_100g", 0)),
                "carbs": float(product.get("nutriments", {}).get("carbohydrates_100g", 0)),
                "fat": float(product.get("nutriments", {}).get("fat_100g", 0)),
                "glycemic_index": None  # Tu możesz dodać własną logikę
            }
            return result
        else:
            return None
    except Exception as e:
        print(f"Błąd pobierania danych z OpenFoodFacts: {e}")
        return None
