import requests

def fetch_repos():
    username = "kronpatel"
    url = f"https://api.github.com/users/{username}/repos"
    
    # Bina kisi secret token ke direct request (Kyunki public data hai)
    response = requests.get(url)
    
    if response.status_code == 200:
        return [repo for repo in response.json() if not repo['fork'] and repo['private'] == False]
    else:
        print(f"Error fetching repos: {response.status_code}")
        return []

def generate_markdown_table(repos):
    markdown_table = "| Name | Description | URL |\n|------|-------------|-----|\n"
    for repo in repos:
        desc = repo.get('description') or 'No description'
        desc = str(desc).replace("|", "-").replace("\n", " ") 
        markdown_table += f"| {repo['name']} | {desc} | [Link]({repo['html_url']}) |\n"
    return markdown_table

def update_readme(table):
    readme_path = "README.md"
    try:
        with open(readme_path, "r", encoding="utf-8") as file:
            content = file.read()

        start_marker = ""
        end_marker = ""
        
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)

        if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
            before_table = content[:start_idx + len(start_marker)]
            after_table = content[end_idx:]
            new_content = before_table + "\n\n" + table + "\n" + after_table
            
            with open(readme_path, "w", encoding="utf-8") as file:
                file.write(new_content)
            print("SUCCESS: Table perfectly generated!")
        else:
            print("ERROR: README me hidden tags nahi mile!")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    repos = fetch_repos()
    if repos:
        table = generate_markdown_table(repos)
        update_readme(table)
    else:
        print("ERROR: Koi repository nahi mili ya net issue!")
