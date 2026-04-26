import os
import requests
import re

def fetch_repos():
    username = "kronpatel"
    url = f"https://api.github.com/users/{username}/repos"
    headers = {}
    token = os.getenv("Profile_REPO_TABLE")
    if token:
        headers['Authorization'] = f"token {token}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return [repo for repo in response.json() if not repo['fork'] and repo['private'] == False]
    else:
        print(f"Error fetching repos: {response.status_code}")
        return []

def generate_markdown_table(repos):
    markdown_table = "| Name | Description | URL |\n|------|-------------|-----|\n"
    for repo in repos:
        desc = repo['description'] if repo['description'] else 'No description'
        desc = desc.replace("|", "-") # Markdown error fix
        markdown_table += f"| {repo['name']} | {desc} | [Link]({repo['html_url']}) |\n"
    return markdown_table

def update_readme(table):
    readme_path = "README.md"
    try:
        with open(readme_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Ye Regex logic table ko humesha correct jagah rakhega aur duplicate nahi hone dega
        pattern = r"().*?()"
        replacement = r"\1\n\n" + table + r"\n\2"
        
        if re.search(pattern, content, re.DOTALL):
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            with open(readme_path, "w", encoding="utf-8") as file:
                file.write(new_content)
            print("README.md updated successfully.")
        else:
            print("Error: Tags and not found!")

    except Exception as e:
        print(f"Error updating README.md: {e}")

if __name__ == "__main__":
    repos = fetch_repos()
    if repos:
        markdown_table = generate_markdown_table(repos)
        update_readme(markdown_table)
