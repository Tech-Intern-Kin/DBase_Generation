import pandas as pd
import ollama
import re

# Load the CSV file
input_file = r"C:\Users\user\Desktop\user1\users.csv"
output_file = r"C:\Users\user\Desktop\user1\suggestions\wine_params_suggestions.csv"

# Initialize the Ollama client
client = ollama.Client()

# Load the CSV data
df = pd.read_csv(input_file, encoding='latin-1')

# Function to generate wine recommendations using Ollama
def generate_recommendation(wines):
    if not wines:
        return None
    
    # Prepare the prompt for Ollama
    prompt = f"I am interested in these wines: {', '.join(wines)}. Suggest 3 more wines with similar parameters."
    
    # Query Ollama's model
    try:
        response = client.generate(
            model='llama_params',  # Replace with your actual model name
            prompt=prompt,
        )
        print(response)
        return response['response'].strip()
        
    except Exception as e:
        response = client.generate(
            model='llama_params',  # Replace with your actual model name
            prompt=prompt,
        )
        print(response)
        print(f"Error generating recommendation: {e}")
        return None

# Process each row in the DataFrame
for index, row in df.iloc[:20].iterrows():
    # print(index, row)
    # Extract existing wines for the customer
    purchased_wines = [wine for wine in [row['Wine 1'], row['Wine 2'], row['Wine 3'], row['Wine 4'], row['Wine 5']] if pd.notna(wine)]
    
    # Generate recommendation only if wines are present
    if len(purchased_wines) > 0:
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
df.to_csv(output_file, index=False, encoding='latin-1')

print(f"Wine recommendations generated and saved to '{output_file}'.")
