import ollama
import csv
import re
import json

client = ollama.Client()

# Updated model and prompt template
model = "llama_food_ingredients"
prompt_template = "Provide details for {food_name}."

# File paths
input_file = r"C:\\Users\\user\\Desktop\\user1\\list_of_food_items.csv"
output_file = r"C:\\Users\\user\\Desktop\\user1\\food_ingredients_structured.csv"

# Read the food item list from the input CSV file
with open(input_file, mode='r', newline='', encoding='latin-1') as infile:
    reader = csv.reader(infile)
    food_list = [row[0] for row in reader]

# Open the output file for writing
with open(output_file, mode='w', newline='', encoding='latin-1') as outfile:
    writer = csv.writer(outfile)
    
    # Write header
    writer.writerow([
        'food name', 'is_dish', 'ingredients', 'category', 'calories', 'protein', 
        'fat', 'carbohydrates', 'fiber', 'sugar', 'dietary suitability', 'processing method', 
        'taste profile', 'common uses'
    ])

    # Ensure valid characters in the food name
    valid_characters = re.compile(r'[A-Za-zÀ-ÿ0-9 &]*')
    processed_food_list = [''.join([str(i) for i in food if valid_characters.match(str(i))]) for food in food_list]

    for food in processed_food_list:
        prompt = prompt_template.format(food_name=food)
        response = client.generate(model=model, prompt=prompt)

        # Extracting JSON response safely
        response_text = response.get('response', '').strip()
        try:
            food_data = json.loads(response_text)  # Convert to Python dictionary
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON response for '{food}'. Skipping.")
            continue  # Skip invalid responses

        # Determine if it's a dish or a base ingredient
        is_dish = "ingredients" in food_data

        # Extract attributes safely
        food_name = food_data.get("food_name", food)
        ingredients = ", ".join(food_data.get("ingredients", [])) if is_dish else ""  # Extract ingredient list if a dish
        category = food_data.get("category", "") if not is_dish else ""
        
        # Nutritional values (for ingredients only)
        nutritional_values = food_data.get("nutritional_values", {}) if not is_dish else {}
        calories = nutritional_values.get("calories", "")
        protein = nutritional_values.get("protein", "")
        fat = nutritional_values.get("fat", "")
        carbohydrates = nutritional_values.get("carbohydrates", "")
        fiber = nutritional_values.get("fiber", "")
        sugar = nutritional_values.get("sugar", "")

        dietary_suitability = ", ".join(food_data.get("dietary_suitability", [])) if not is_dish else ""
        processing_method = food_data.get("processing_method", "") if not is_dish else ""
        taste_profile = ", ".join(food_data.get("taste_profile", [])) if not is_dish else ""
        common_uses = ", ".join(food_data.get("common_uses", [])) if not is_dish else ""

        # Write data to CSV
        writer.writerow([
            food_name, "Yes" if is_dish else "No", ingredients, category, calories, 
            protein, fat, carbohydrates, fiber, sugar, dietary_suitability, 
            processing_method, taste_profile, common_uses
        ])

print("Done")
