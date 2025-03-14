import pandas as pd
import ollama

# Specify the input and output CSV files
input_file = 'input.csv'
output_file = 'wine_recommendations.csv'

# Initialize Ollama client
client = ollama.Client()

# Load the CSV data
df = pd.read_csv(input_file)

# Function to generate wine recommendations using Ollama
def generate_wine_recommendation(profile):
    # Create the prompt based on the user's taste profile
    prompt = (
        f"A user has the following taste profile:\n"
        f"- Budget: {profile.get('Budget', 'Not specified')}\n"
        f"- Difficulty Picking: {profile.get('Difficulty_Picking', 'Not specified')}\n"
        f"- Food: {profile.get('Food', 'Not specified')}\n"
        f"- Grape Breed: {profile.get('GrapeBreed', 'Not specified')}\n"
        f"- Occasion: {profile.get('Occasion', 'Not specified')}\n"
        f"- Occasions: {profile.get('Occasions', 'Not specified')}\n"
        f"- Savant: {profile.get('Savant', 'Not specified')}\n"
        f"- Scenario: {profile.get('Scenario', 'Not specified')}\n"
        f"- Store Purchase Preference: {profile.get('StorePurchase', 'Not specified')}\n"
        f"- Why Not Like: {profile.get('Why_not_like', 'Not specified')}\n"
        f"- Wine Type: {profile.get('Wine Type', 'Not specified')}\n"
        f"- Wine Purchase Frequency: {profile.get('WinePurchaseFreq', 'Not specified')}\n"
        f"- Wines Not Liking: {profile.get('Wines_not_liking', 'Not specified')}\n\n"
        f"Based on this profile, suggest 3 wines that match and provide a short reason for each recommendation."
    )

    # Query Ollama's model
    try:
        response = client.generate(
            model='wine-recommendation',  # Replace with your actual model name
            prompt=prompt,
            temperature=0.7,
            max_tokens=200
        )
        return response['text'].strip()
    except Exception as e:
        print(f"Error generating recommendation: {e}")
        return "No recommendation generated due to an error."

# Apply the recommendation function to each row
df['Wine Recommendations'] = df.apply(lambda row: generate_wine_recommendation(row), axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"Wine recommendations generated and saved to '{output_file}'.")
