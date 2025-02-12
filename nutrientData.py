import requests
import json

API_KEY = "3YfUTCOt0J3CYbBYLldqSZdbllJe71iqiMh939TT"

def search_food(food_name, num_results=100):
    all_food_data = []  # List to hold all food data in one dataset
    page = 1
    while True:
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&api_key={API_KEY}&pageSize={num_results}&page={page}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if "foods" in data and data["foods"]:
                all_food_data.extend(data["foods"])  # Add all food data to the list
                # Check if there is another page of results
                if len(data["foods"]) < num_results:
                    break  # Exit loop if no more data is available
                page += 1
            else:
                print("No food data found.")
                break
        else:
            print("Error:", response.status_code)
            break

    # Save the unified food dataset to a JSON file
    with open(f"{food_name}_all_data.json", "w") as f:
        json.dump(all_food_data, f, indent=4)

    print(f"Unified food data saved to {food_name}_all_data.json")

search_food("chicken breast", num_results=100) 
