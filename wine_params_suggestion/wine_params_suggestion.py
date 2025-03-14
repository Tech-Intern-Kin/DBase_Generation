import pandas as pd
import ollama
import re

# Load the CSV file
input_file = 'input.csv'
output_file = 'output.csv'

# Initialize the Ollama client
client = ollama.Client()

# Load the CSV data
df = pd.read_csv(input_file)

# Function to generate wine recommendations using Ollama
def generate_recommendation(wines):
    if not wines:
        return None
    
    # Prepare the prompt for Ollama
    prompt = f"I have purchased these wines: {', '.join(wines)}. Suggest 3 more wines with similar parameters."
    
    # Query Ollama's model
    try:
        response = client.generate(
            model='wine-recommendation',  # Replace with your actual model name
            prompt=prompt,
            temperature=0.7,
            max_tokens=150
        )
        return response['text'].strip()
    except Exception as e:
        print(f"Error generating recommendation: {e}")
        return None

# Process each row in the DataFrame
for index, row in df.iterrows():
    # Extract existing wines for the customer
    purchased_wines = [wine for wine in [row['Wine 1'], row['Wine 2'], row['Wine 3'], row['Wine 4'], row['Wine 5']] if pd.notna(wine)]
    
    # Generate recommendation only if wines are present
    if purchased_wines:
        recommendation = generate_recommendation(purchased_wines)
        
        # Find the next empty column to store the recommendation
        for i in range(1, 10):
            col_name = f'Recommendation {i}'
            if col_name not in df.columns:
                df[col_name] = ''
            
            if pd.isna(row.get(col_name)) or row.get(col_name) == '':
                df.at[index, col_name] = recommendation
                break

# Save the updated DataFrame to a new CSV file
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"Wine recommendations generated and saved to '{output_file}'.")
