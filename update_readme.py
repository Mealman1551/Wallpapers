import requests
import os
from urllib.parse import quote

# Configuratie
repo_owner = "mealman1551"
repo_name = "wallpapers"
branch = "main"  # Hoofdtak, verander naar 'master' als dat de standaard is
readme_path = r"D:\Github Git Repo clones\Wallpapers\README.md"  # Exacte pad naar je README.md bestand
github_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/{branch}?recursive=1"  # Recursief door alle mappen heen

# Functie om afbeeldingen-URLs uit de repo te krijgen
def get_image_urls():
    response = requests.get(github_api_url)
    if response.status_code == 200:
        data = response.json()
        image_urls = []

        # Loop door de bestanden in de repo
        for file in data['tree']:
            # Alleen afbeelding-bestanden (jpg, png, jpeg)
            if file['path'].endswith(('.jpg', '.png', '.jpeg')):
                # Encodeer het pad om spaties correct te verwerken
                encoded_path = quote(file['path'])
                raw_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{encoded_path}"
                image_urls.append(raw_url)

        # Print de afbeelding-URLs voor controle
        print(f"Afbeeldingen gevonden: {image_urls}")
        return image_urls
    else:
        print("Error bij het ophalen van de bestanden.")
        return []

# Functie om de README.md bij te werken met de nieuwe afbeeldingen
def update_readme(image_urls):
    if not image_urls:
        print("Geen afbeeldingen gevonden om toe te voegen aan README.md.")
        return

    # Lees de bestaande README.md
    with open(readme_path, "r", encoding="utf-8") as readme_file:
        readme_content = readme_file.readlines()

    # Zoek het punt waar de nieuwe content moet worden toegevoegd (na de bestaande inhoud)
    # We voegen de nieuwe afbeeldingen toe direct onder de titel en andere informatie
    markdown_start = "| Column 1 | Column 2 | Column 3 | Column 4 |\n|---------|---------|---------|---------|\n"
    markdown_row = "|"
    for i, url in enumerate(image_urls):
        markdown_row += f" ![Image]({url}) |"
        if (i + 1) % 4 == 0:
            markdown_start += markdown_row + "\n"
            markdown_row = "|"
    if markdown_row != "|":
        markdown_start += markdown_row + "\n"

    # Zoek de eerste sectie van de README om de nieuwe inhoud toe te voegen
    # Dit voegt de markdown direct onder de bestaande tekst toe
    readme_content.append(markdown_start)

    # Schrijf de bijgewerkte README.md
    with open(readme_path, "w", encoding="utf-8") as readme_file:
        readme_file.writelines(readme_content)

    print("README.md succesvol bijgewerkt met de nieuwe afbeeldingen!")

# Main
if __name__ == "__main__":
    print("Zoeken naar afbeeldingen in de GitHub repository...")
    image_urls = get_image_urls()
    update_readme(image_urls)