import ollama
import csv
import re
import json

client = ollama.Client()

# Updated model and prompt template
model = "llama_wine_ingredients"
prompt_template = """Given the wine {wine_name}, provide a structured breakdown of its key ingredients. 
Include grape variety, additives, fermentation-related ingredients, and any aging-related components. 
If applicable, mention common fining agents or preservatives. Output the information in a structured JSON format."""

# File paths
input_file = r"C:\\Users\\user\\Desktop\\user1\\list_of_wines.csv"
output_file = r"C:\\Users\\user\\Desktop\\user1\\wine_ingredients_structured.csv"

# Read the wine list from the input CSV file
with open(input_file, mode='r', newline='', encoding='latin-1') as infile:
    reader = csv.reader(infile)
    wine_list = [row[0] for row in reader]

# Open the output file for writing
with open(output_file, mode='w', newline='', encoding='latin-1') as outfile:
    writer = csv.writer(outfile)
    
    # Write header
    writer.writerow(['wine name', 'grape varieties', 'additives', 'fermentation agents', 'aging components', 'fining agents'])

    # Ensure valid characters in the wine name
    valid_characters = re.compile(r'[A-Za-zÀ-ÿ0-9 &]*')
    processed_wine_list = [''.join([str(i) for i in wine if valid_characters.match(str(i))]) for wine in wine_list]

    for wine in processed_wine_list:
        prompt = prompt_template.format(wine_name=wine)
        response = client.generate(model=model, prompt=prompt)

        # Extracting JSON response safely
        response_text = response.get('response', '').strip()
        try:
            ingredients_data = json.loads(response_text)  # Convert to Python dictionary
        except json.JSONDecodeError:
            ingredients_data = {"error": "Invalid JSON response"}  # Handle errors gracefully

        # Extract attributes safely
        wine_name = ingredients_data.get("wine_name", wine)
        grape_varieties = ", ".join(ingredients_data.get("ingredients", []))
        additives = ", ".join(ingredients_data.get("additives", []))
        fermentation_agents = ", ".join(ingredients_data.get("fermentation_agents", []))
        aging_components = ", ".join(ingredients_data.get("aging_components", []))
        fining_agents = ", ".join(ingredients_data.get("processing_agents", []))

        # Write data to CSV
        writer.writerow([wine_name, grape_varieties, additives, fermentation_agents, aging_components, fining_agents])

print("Done")
