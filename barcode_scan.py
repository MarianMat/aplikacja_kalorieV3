import requests

def fetch_product_data(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        if data.get("status") == 1:
            product = data["product"]
            nutriments = product.get("nutriments", {})
            return {
                "product_name": product.get("product_name", "Brak nazwy"),
                "calories": float(nutriments.get("energy-kcal_100g", 0.0)),
                "protein": float(nutriments.get("proteins_100g", 0.0)),
                "fat": float(nutriments.get("fat_100g", 0.0)),
                "carbs": float(nutriments.get("carbohydrates_100g", 0.0))
            }
    except Exception:
        pass
    return None
