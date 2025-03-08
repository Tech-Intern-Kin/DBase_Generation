import os
import pandas as pd
import ollama
from github import Github

# GitHub credentials and repository information
github_token = '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'
input_repo_owner = 'RoaldSchuring'
input_repo_name = 'studying_grape_styles'
input_csv_path = 'data/all_scraped_wine_info_chardonnay.csv'  # Path within the input repository
output_repo_owner = 'Tech-Intern-Kin'
output_repo_name = 'DBase_Generation'
output_csv_path = ''  # Path within the output repository

# Path to the locally downloaded llama3.1 model
model_path = '' # to find llama3.1 path

# Define the prompt template
prompt_template = "I have this wine {wine_name}. What food/meal goes well with {wine_name}?"

# Load the Ollama model
ollama_model = Llama(model_path=model_path)

# Function to generate LLM response for a given wine name
def generate_llm_response(wine_name):
    prompt = prompt_template.format(wine_name=wine_name)
    llm_response = ollama_model.predict(prompt)
    return llm_response

# Function to authenticate and retrieve file content from GitHub repository
def get_github_file_content(repo, file_path):
    contents = repo.get_contents(file_path)
    return contents.decoded_content.decode('utf-8')

# Function to authenticate and create/update file content in GitHub repository
def update_github_file_content(repo, file_path, new_content, commit_message):
    contents = repo.get_contents(file_path)
    repo.update_file(contents.path, commit_message, new_content, contents.sha)

# Authenticate with GitHub using token
g = Github(github_token)
input_repo = g.get_user(input_repo_owner).get_repo(input_repo_name)
output_repo = g.get_user(output_repo_owner).get_repo(output_repo_name)

# Get input dataset from GitHub repository
input_csv_content = get_github_file_content(input_repo, input_csv_path)

# Read input dataset CSV
df = pd.read_csv(io.StringIO(input_csv_content))

# Iterate over each wine name in the dataset and generate LLM responses
responses = []
for wine_name in df['WineName']:
    llm_response = generate_llm_response(wine_name)
    responses.append({
        'WineName': wine_name,
        'LLMResponse': llm_response
    })

# Convert responses to DataFrame
output_df = pd.DataFrame(responses)

# Convert DataFrame to CSV content
output_csv_content = output_df.to_csv(index=False)

# Update output dataset in the GitHub repository
update_github_file_content(output_repo, output_csv_path, output_csv_content, "Updated output dataset")

print("Output dataset updated in the GitHub repository.")
