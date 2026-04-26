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

    # Agar tags milte hain toh unke beech table daalo
    if start_tag in content and end_tag in content:
        start_parts = content.split(start_tag)
        before_tag = start_parts[0]
        after_tag_part = start_parts[1].split(end_tag)[1]
        
        new_content = before_tag + start_tag + "\n\n" + table_content + "\n\n" + end_tag + after_tag_part
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Success: Table updated!")
    else:
        # Agar tags nahi mile, toh file ke end mein tags ke saath table chipka do
        print("Tags not found, appending to the end of file...")
        new_content = content + f"\n\n{start_tag}\n\n{table_content}\n\n{end_tag}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

if __name__ == "__main__":
    repos = fetch_repos()
    if repos:
        markdown_table = generate_markdown_table(repos)
        update_readme(markdown_table)
