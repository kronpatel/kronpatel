import requests

def fetch_repos():
    username = "kronpatel"
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return [repo for repo in response.json() if not repo['fork'] and not repo['private']]
    return []

def generate_markdown_table(repos):
    table = "| Name | Description | URL |\n|------|-------------|-----|\n"
    for repo in repos:
        desc = repo.get('description') or 'No description'
        table += f"| **{repo['name']}** | {desc} | [Link]({repo['html_url']}) |\n"
    return table

def update_readme(table_content):
    file_path = "README.md"
    start_marker = ""
    end_marker = ""

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if start_marker in content and end_marker in content:
        # Markers ke beech ka hissa replace karna
        parts = content.split(start_marker)
        before = parts[0]
        after = parts[1].split(end_marker)[1]
        
        new_content = before + start_marker + "\n\n" + table_content + "\n\n" + end_marker + after
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Success: Table updated!")
    else:
        print("Error: Markers not found!")

if __name__ == "__main__":
    repos = fetch_repos()
    if repos:
        markdown_table = generate_markdown_table(repos)
        update_readme(markdown_table)
