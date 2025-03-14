import pandas as pd
import ollama
import time

# Specify the input and output CSV files
input_file = r"C:\Users\user\Desktop\user1\users.csv"
output_file = r"C:\Users\user\Desktop\user1\suggestions\taste_profile_suggestions.csv"

# Initialize Ollama client
client = ollama.Client()

# Load the CSV data
df = pd.read_csv(input_file, encoding='latin-1')

# Function to generate wine recommendations using Ollama
def generate_wine_recommendation(profile):
    # Create the prompt based on the user's taste profile
    prompt = (
        f"Based on my taste profile, suggest 3 wines that match and provide a short reason for each recommendation."
        f"- Budget: {profile.get('Budget', 'Not specified')}\n"
        f"- Difficulty Picking: {profile.get('Difficulty_Picking', 'Not specified')}\n"
        f"- Food: {profile.get('Food', 'Not specified')}\n"
        f"- Grape Breed: {profile.get('GrapeBreed', 'Not specified')}\n"
        f"- Occasions: {profile.get('Occasions', 'Not specified')}\n"
        f"- Expert-level suggestions: {profile.get('Savant', 'Not specified')}\n"
        f"- Store Purchase Preference: {profile.get('StorePurchase', 'Not specified')}\n"
        f"- Wine Type: {profile.get('Wine Type', 'Not specified')}\n"
        f"- Wine Purchase Frequency: {profile.get('WinePurchaseFreq', 'Not specified')}\n"
    )

    # Query Ollama's model
    try:
        response = client.generate(
            model='llama_taste',  # Replace with your actual model name
            prompt=prompt,
        )
        return response['response'].strip()
    
    except Exception as e:
        print(f"Error generating recommendation: {e}")
        return "No recommendation generated due to an error."

def prompts(profile):
    # Create the prompt based on the user's taste profile
    prompt = (
        f"A user has the following taste profile:\n"
        f"- Budget: {profile.get('Budget', 'Not specified')}\n"
        f"- Difficulty Picking: {profile.get('Difficulty_Picking', 'Not specified')}\n"
        f"- Food: {profile.get('Food', 'Not specified')}\n"
        f"- Grape Breed: {profile.get('GrapeBreed', 'Not specified')}\n"
        f"- Occasions: {profile.get('Occasions', 'Not specified')}\n"
        f"- Expert-level suggestions: {profile.get('Savant', 'Not specified')}\n"
        f"- Scenario: {profile.get('Scenario', 'Not specified')}\n"
        f"- Store Purchase Preference: {profile.get('StorePurchase', 'Not specified')}\n"
        f"- Dislike: {profile.get('Why_not_like', 'Not specified')}\n"
        f"- Wine Type: {profile.get('Wine Type', 'Not specified')}\n"
        f"- Wine Purchase Frequency: {profile.get('WinePurchaseFreq', 'Not specified')}\n"
        f"- Wines Not Liking: {profile.get('Wines_not_liking', 'Not specified')}\n\n"
        f"Based on this profile, suggest 3 wines that match and provide a short reason for each recommendation.\n"
        f"nan means not specified, so just use the non-nan inputs as reference"
    )
    return prompt

def retry_recommendation(row, retries=3):
    for attempt in range(retries):
        recommendation = generate_wine_recommendation(row)
        if len(recommendation) > 0:
            return recommendation
        time.sleep(1)
    return "No recommendation generated after 3 attempts"

# Apply the recommendation function to each row
df.loc[68:71,'Wine Recommendations'] = df.loc[68:71].apply(
    lambda row: retry_recommendation(row), axis=1)
df.loc[68:71,'Prompt'] = df.loc[68:71].apply(lambda row: prompts(row), axis=1)

# Save the updated DataFrame to a new CSV file
try:
    df.to_csv(output_file, index=False, encoding='latin-1')
except:
    UnicodeEncodeError
    try:
        df.to_csv(output_file, index=False, encoding='utf-8')
    except:
        print("failed to save file")
    

    

print(f"Wine recommendations generated and saved to '{output_file}'.")
