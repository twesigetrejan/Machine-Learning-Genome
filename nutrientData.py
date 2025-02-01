
import requests

API_KEY = "3YfUTCOt0J3CYbBYLldqSZdbllJe71iqiMh939TT"

def search_food(food_name):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&api_key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "foods" in data:
            for food in data["foods"][:5]:
                print(f"\nFood: {food['description']}")
                for nutrient in food.get("foodNutrients", []):
                    print(f"  - {nutrient['nutrientName']}: {nutrient['value']} {nutrient.get('unitName', '')}")
        else:
            print("No food data found.")
    else:
        print("Error:", response.status_code)

search_food("chicken breast")
