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

        # Is baar hum thoda flexible search kar rahe hain
        start_marker = ""
        end_marker = ""
        
        if start_marker in content and end_marker in content:
            parts = content.split(start_marker)
            first_half = parts[0] + start_marker
            second_half = parts[1].split(end_marker)[1]
            
            new_content = first_half + "\n\n" + table + "\n" + end_marker + second_half
            
            with open(readme_path, "w", encoding="utf-8") as file:
                file.write(new_content)
            print("SUCCESS: Table generated perfectly!")
        else:
            print("ERROR: Hidden tags missing! Check README for ")

    except Exception as e:
        print(f"ERROR: {e}")
