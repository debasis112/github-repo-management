import os
import requests
import json

# user config details
USERNAME = os.getenv('GH_USERNAME')
USER_EMAIL = os.getenv('GH_USER_EMAIL')
USER_NAME = os.getenv('GH_USER_NAME')

# GitHub Token
GH_TOKEN = os.getenv('GH_TOKEN')

# List of repositories with their properties
repositories = [
    {"name": "cloud-secrets", "description": "This is the repository for secrets.", "private": True},
    {"name": "aws-cloud-resources", "description": "This repository is for aws resources.", "private": False},
    {"name": "azure-cloud-setup", "description": "This repository is for azure resources.", "private": True},
    {"name": "terraform-resources", "description": "This repository is for management of terraform project and workspace.", "private": True},
    {"name": "web-pages-docker-push", "description": "This repository is for web page to create and push image to docker hub.", "private": False},
    {"name": "web-pages-acr-push", "description": "This repository is for web page to pull Docker image and push to ACR.", "private": False},
    # Add more repositories here
]

for repo in repositories:
    REPO_NAME = repo['name']
    DESCRIPTION = repo['description']
    PRIVATE = repo['private']
    
    # Check if the repository already exists
    repo_check_url = f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}'
    repo_check_response = requests.get(repo_check_url, auth=(USERNAME, GH_TOKEN))
    
    if repo_check_response.status_code == 200:
        print(f'Repository {REPO_NAME} already exists. Skipping creation.')
        continue  # Skip to the next repository if it already exists
    
    # Create the repository
    url = f'https://api.github.com/user/repos'
    data = {
        "name": REPO_NAME,
        "description": DESCRIPTION,
        "private": PRIVATE
    }

    response = requests.post(url, auth=(USERNAME, GH_TOKEN), data=json.dumps(data))
    if response.status_code == 201:
        print(f'Successfully created repository {REPO_NAME}')
    else:
        print(f'Failed to create repository: {response.json()}')
        continue

    # Configure Git
    os.system(f'git config --global user.email "{USER_EMAIL}"')
    os.system(f'git config --global user.name "{USER_NAME}"')

    # Clone the repository using GH_TOKEN for authentication
    clone_url = f'https://{USERNAME}:{GH_TOKEN}@github.com/{USERNAME}/{REPO_NAME}.git'
    os.system(f'git clone {clone_url}')

    # Change to the cloned repository directory
    os.chdir(REPO_NAME)

    # Create a README.md file
    with open('README.md', 'w') as f:
        f.write(f'# {REPO_NAME}\n\n{DESCRIPTION}')

    # Initialize git and commit the README file
    os.system('git init')
    os.system('git add .')
    os.system('git commit -m "Initial commit"')

    # Push the changes to GitHub
    os.system(f'git remote add origin {clone_url}')
    os.system('git branch -M main')
    os.system('git push -u origin main')

    # Go back to the parent directory for the next repo
    os.chdir('..')
