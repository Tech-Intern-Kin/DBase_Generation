import pandas as pd
import re

input_file = r"C:\Users\user\Desktop\user1\suggestions\taste_profile_suggestions_b.csv"
output_file = r"C:\Users\user\Desktop\user1\suggestions\taste_profile_suggestions_clean.csv"

# df = pd.read_csv(input_file, encodingISO-8859-1", errors='replace')

with open(input_file, 'r', encoding = "ISO-8859-1", errors='replace') as file:
    df = pd.read_csv(file)

def clean_recommendation(text):
    if isinstance(text,str):
        print(re.sub(r'^.*?(?=1)', '', text))
    match = re.search(r'(1\..*)', text, re.DOTALL)
        # return re.sub(r'^.*?(?=1)', '', text)
    return match.group(1) if match else text
    # return text

df['Wine Recommendations'] = df['Wine Recommendations'].apply(clean_recommendation)
df.to_csv(output_file, index=False)

print("Done")