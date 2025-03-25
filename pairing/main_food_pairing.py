import ollama
import csv
import re

client = ollama.Client()

model = "llama"
prompt_template = "I have this fine food {food_name}, what wine would you recommend pairing it with, and why?"


input_file = r"C:\Users\user\Desktop\user1\list_of_foods.csv"
output_file = r"C:\Users\user\Desktop\user1\wine_recommendations.csv"
with open(input_file, mode='r', newline='') as infile:
    reader = csv.reader(infile)
    food_list = [row[0] for row in reader]

with open(output_file, mode='w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['food name', 'wine recommendation'])
    valid_characters = re.compile(r'[A-Za-zÀ-ÿ0-9 &]*') 
    processed_food_list = [''.join([str(i) for i in food if valid_characters.match(str(i))]) for food in food_list]  

    for food in processed_food_list:
        prompt = prompt_template.format(food_name = food)
        response = client.generate(model=model, prompt=prompt)
        response = response.get('response', '')
        writer.writerow([food, response])


print("Done")