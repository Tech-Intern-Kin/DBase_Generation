import ollama
import csv
import re

client = ollama.Client()

model = "llama_general"

# Prompt templates for each field
PROMPTS = {
    'grape_varieties': "List the grape varieties used in {wine_name}. Respond with a simple comma-separated list.",
    'additives': "What additives are commonly used in making {wine_name}? Respond with a comma-separated list.",
    'fermentation_agents': "What fermentation agents are used in the production of {wine_name}? Respond with a comma-separated list.",
    'aging_components': "Describe the aging components used for {wine_name}. Respond with a comma-separated list.",
    'fining_agents': "What fining agents are typically used in {wine_name}? Respond with a comma-separated list."
}

# File paths
input_file = r"C:\\Users\\user\\Desktop\\user1\\list_of_wines.csv"
output_file = r"C:\\Users\\user\\Desktop\\user1\\wine_ingredients_structured.csv"

# Read wine names
with open(input_file, mode='r', newline='', encoding='latin-1') as infile:
    reader = csv.reader(infile)
    wine_list = [row[0].strip() for row in reader]

# Write results
with open(output_file, mode='w', newline='', encoding='latin-1') as outfile:
    writer = csv.writer(outfile)
    writer.writerow([
        'wine name',
        'grape varieties',
        'additives',
        'fermentation agents',
        'aging components',
        'fining agents'
    ])

    for wine in wine_list:
        print(f"Processing: {wine}")
        row = [wine]

        for field, prompt_template in PROMPTS.items():
            prompt = prompt_template.format(wine_name=wine)
            try:
                response = client.generate(model=model, prompt=prompt)
                result = response.get('response', '').strip()
                # Basic cleanup
                result = result.replace('\n', ' ').strip()
            except Exception as e:
                print(f"Error while processing '{field}' for '{wine}': {e}")
                result = "ERROR"
            row.append(result)

        writer.writerow(row)

print("Done.")
