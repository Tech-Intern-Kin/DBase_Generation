import ollama
import csv
import re

client = ollama.Client()

model = "llama"
prompt_template = "I have this fine wine {wine_name}, what food would you recommend pairing it with, and why?"

input_file = r"C:\\Users\\user\\Desktop\\user1\\list_of_wines.csv"
output_file = r"C:\\Users\\user\\Desktop\\user1\\food_recommendations.csv"

with open(input_file, mode='r', newline='') as infile:
    reader = csv.reader(infile)
    wine_list = [row[0] for row in reader]

with open(output_file, mode='w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['wine name', 'food recommendation'])
    valid_characters = re.compile(r'[A-Za-zÀ-ÿ0-9 &]*')
    processed_wine_list = [''.join([str(i) for i in wine if valid_characters.match(str(i))]) for wine in wine_list]

    for wine in processed_wine_list:
        prompt = prompt_template.format(wine_name=wine)
        response = client.generate(model=model, prompt=prompt)
        response = response.get('response', '')
        writer.writerow([wine, response])

print("Done")
