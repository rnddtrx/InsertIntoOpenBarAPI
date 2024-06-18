from time import sleep

import requests
import json
import random
import uuid

def insert_ingredient(name):
    url = "http://localhost:8080/api/ingredient/ingredient"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "name": name
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("Ingredient inserted successfully.")
        else:
            print("Failed to insert ingredient. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# def generate_random_recipe_name():
#     try:
#         response = requests.get("https://random-word-api.herokuapp.com/word?number=2")
#         if response.status_code == 200:
#             words = response.json()
#             return ' '.join(words)
#         else:
#             print("Failed to fetch random words. Status code:", response.status_code)
#     except requests.exceptions.RequestException as e:
#         print("Error:", e)


def get_random_word():
    url = "https://api.datamuse.com/words"
    params = {
        'ml': 'food'  # Use a common word related to food to get a list of similar words
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            words = response.json()
            if words:
                # Randomly select a word from the list
                word = random.choice(words).get("word")
                return word
            else:
                print("No words found.")
                return None
        else:
            print("Failed to fetch word. Status code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def generate_random_recipe_name():
    words = [get_random_word() for _ in range(2)]
    if all(words):
        return ' '.join(words)
    else:
        return None

def generate_random_step_description():
    try:
        response = requests.get("https://baconipsum.com/api/?type=all-meat&sentences=1&start-with-lorem=1")
        if response.status_code == 200:
            step_text = response.json()[0]
            return step_text
        else:
            print("Failed to fetch random step description. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

def generate_random_recipe(ingredients):
    num_ingredients = random.randint(3, 7)
    recipe_name = generate_random_recipe_name() or "Random Recipe"
    recipe_description = "A delicious random recipe"
    recipe_image = "random_recipe_image.jpg"
    ingredient_quantities = []

    # Randomly select ingredients
    for _ in range(num_ingredients):
        ingredient = random.choice(ingredients)
        quantity = random.uniform(0.5, 3.0)  # Random quantity between 0.5 and 3.0
        unit = "oz"  # Assuming the unit is ounces for simplicity
        ingredient_quantities.append({"ingredient": ingredient, "quantity": quantity, "unit": unit})

    # Generate random steps
    num_steps = random.randint(3, 5)
    steps = []
    for i in range(num_steps):
        step_description = generate_random_step_description() or "Lorem Ipsum"
        is_first_step = (i == 0)
        is_last_step = (i == num_steps - 1)
        step = {
            "description": step_description,
            "firstStep": is_first_step,
            "lastStep": is_last_step
        }
        steps.append(step)

    return {"name": recipe_name, "description": recipe_description, "image": recipe_image, "quantities": ingredient_quantities, "steps": steps}

def find_ingredient_id(ingredient_name):
    url = "http://localhost:8080/api/ingredient/ingredient?name=" + ingredient_name
    try:
        response = requests.get(url)
        if response.status_code == 200:
            ingredient_data = response.json()
            if ingredient_data:
                #print(ingredient_data)
                return ingredient_data["id"]
            else:
                print("Ingredient not found:", ingredient_name)
        else:
            print("Failed to find ingredient. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

def insert_recipe(recipe_data):
    url = "http://localhost:8080/api/recipe/recipe"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "name": recipe_data["name"],
        "description": recipe_data["description"],
        "image": recipe_data["image"],
        "quantities": recipe_data["quantities"],
        "steps": recipe_data["steps"]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            None
            #print("Recipe inserted successfully")
        else:
            print("Failed to insert recipe. Status code:", response.status_code)
            print(recipe_data)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

ingredients = [
    "Vodka", "Gin", "Rum", "Tequila", "Whiskey", "Bourbon", "Brandy", "Cointreau",
    "Kahlua", "Baileys", "Raspberry Liqueur", "Cranberry Juice", "Orange Juice",
    "Pineapple Juice", "Lemon Juice", "Lime Juice", "Simple Syrup", "Grenadine",
    "Creme de Menthe", "Soda Water", "Tonic Water", "Cola", "Ginger Beer",
    "Coconut Cream", "Amaretto", "Peach Schnapps", "Angostura Bitters",
    "Peychaud's Bitters", "Prosecco", "Champagne", "Sparkling Wine",
    "Campari", "Triple Sec", "Blue Curacao", "Maraschino Liqueur", "Irish Cream",
    "Whipped Cream", "Coconut Milk", "Peach Puree", "Mint Leaves", "Basil Leaves",
    "Cucumber", "Ginger", "Vanilla Extract", "Cinnamon Syrup", "Maple Syrup",
    "Honey Syrup", "Lavender Syrup", "Elderflower Liqueur", "Apple Cider",
    "Cider Brandy", "Pear Liqueur", "Pomegranate Juice", "Cucumber Juice",
    "Passion Fruit Puree", "Strawberry Puree", "Watermelon Juice", "Kiwi Juice",
    "Mango Puree", "Lychee Juice", "Papaya Juice", "Coconut Water", "Aperol",
    "Sake", "Soju", "Mint Syrup", "Rosemary Syrup", "Bacon Infused Bourbon",
    "Jalapeno Infused Tequila", "Cilantro Infused Vodka", "Lavender Gin",
    "Chili Pepper Vodka", "Green Chartreuse", "Grand Marnier", "Frangelico",
    "Pisco", "Sherry", "St. Germain Elderflower Liqueur", "Absinthe", "Lillet Blanc",
    "Dry Vermouth", "Sweet Vermouth", "Marsala Wine", "White Wine", "Red Wine",
    "Port Wine", "Chambord", "Midori", "Sambuca", "Amarula", "Ouzo", "Galliano",
    "Chartreuse", "Irish Whiskey", "Japanese Whisky", "Canadian Whisky", "Rye Whiskey",
    "Scotch Whisky", "Mezcal", "Anise Liqueur", "Cachaca", "Aquavit"
]

for i in ingredients:
    None
    insert_ingredient(i)

for _ in range(100):
    random_recipe = generate_random_recipe(ingredients)

    #print(random_recipe)

    # Find ingredient IDs
    ingredient_ids = []
    for ingredient_data in random_recipe["quantities"]:
        ingredient_name = ingredient_data["ingredient"]
        #print(ingredient_name)
        ingredient_id = find_ingredient_id(ingredient_name)
        if ingredient_id:
            ingredient_data["ingredient"] = {"id": ingredient_id}
            ingredient_ids.append(ingredient_id)

    insert_recipe(random_recipe)
    #sleep()