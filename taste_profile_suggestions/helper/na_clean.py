import pandas as pd

input_file = r"C:\Users\user\Desktop\user1\users.csv"
output_file = r"C:\Users\user\Desktop\user1\users_clean.csv"

df = pd.read_csv(input_file, encoding='latin-1')

df.fillna("Not specified", inplace=True)
df.replace(r'^\s*$', 'Not Specified', regex=True, inplace=True)

df.to_csv(output_file, index=False, encoding='latin-1')

print('done')