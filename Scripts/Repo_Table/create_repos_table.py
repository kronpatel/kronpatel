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

    # Direct strings use kar rahe hain bina kisi variable ke
    if "" in content and "" in content:
        # Split logic ko ekdum simple rakha hai
        before = content.split("")[0]
        after = content.split("")[1]
        
        new_content = before + "\n\n" + table_content + "\n\n" + after
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Success: README updated with table!")
    else:
        # Agar tags nahi mile toh safe side ke liye end mein append kar dega
        print("Markers not found, appending to end...")
        new_content = content + "\n\n\n\n" + table_content + "\n\n"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

if __name__ == "__main__":
    repos = fetch_repos()
    if repos:
        markdown_table = generate_markdown_table(repos)
        update_readme(markdown_table)
