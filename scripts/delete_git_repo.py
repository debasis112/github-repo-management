import os
import requests

# Replace the following variables with your own details
USERNAME = os.getenv('GH_USERNAME')

# GitHub Token stored in environment variables in GitHub Actions
GH_TOKEN = os.getenv('GH_TOKEN')

# List of repositories you want to delete
repositories_to_delete = [
    "test-11",
    "test-12",
    # Add more repositories here
]

for repo_name in repositories_to_delete:
    # API URL to check if the repository exists
    check_url = f'https://api.github.com/repos/{USERNAME}/{repo_name}'
    
    # Check if the repository exists
    check_response = requests.get(check_url, auth=(USERNAME, GH_TOKEN))
    
    if check_response.status_code == 404:
        print(f'Repository {repo_name} does not exist or is already deleted.')
        continue  # Skip to the next repository if it doesn't exist
    
    # API URL to delete the repository
    delete_url = f'https://api.github.com/repos/{USERNAME}/{repo_name}'
    
    # Make the DELETE request
    response = requests.delete(delete_url, auth=(USERNAME, GH_TOKEN))
    
    if response.status_code == 204:
        print(f'Successfully deleted repository {repo_name}')
    else:
        print(f'Failed to delete repository {repo_name}: {response.json()}')
