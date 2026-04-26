import os
import requests

def fetch_repos():
    username = "kronpatel"
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return [repo for repo in response.json() if not repo['fork'] and repo['private'] == False]
    return []

def generate_markdown_table(repos):
    table = "| Name | Description | URL |\n|------|-------------|-----|\n"
    for repo in repos:
        desc = repo.get('description') or 'No description'
        table += f"| **{repo['name']}** | {desc} | [Link]({repo['html_url']}) |\n"
    return table

def update_readme(table_content):
    file_path = "README.md"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = ""
    end_tag = ""

    if start_tag in content and end_tag in content:
        # Purani table hatakar nayi table fit karna
        before = content.split(start_tag)[0]
        after = content.split(end_tag)[1]
        new_content = before + start_tag + "\n\n" + table_content + "\n\n" + end_tag + after
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Success: Table updated!")
    else:
        print("Error: Tags not found in README!")

if __name__ == "__main__":
    repos = fetch_repos()
    if repos:
        markdown_table = generate_markdown_table(repos)
        update_readme(markdown_table)
