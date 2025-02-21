import os
import requests

# Het juiste pad naar je lokale repository
repo_path = r"D:/Github Git Repo clones/Wallpapers"  # Pas dit pad aan

# Functie om de raw URL van een afbeelding te krijgen, met spaties omgezet naar %20
def get_raw_url(img_path):
    # Vervang het lokale pad door de GitHub raw URL
    relative_path = img_path.replace(repo_path + os.sep, '').replace(os.sep, '/')
    
    # Vervang spaties door %20 voor de juiste URL-encoding
    relative_path = relative_path.replace(' ', '%20')
    
    image_url = f"https://raw.githubusercontent.com/Mealman1551/Wallpapers/refs/heads/main/{relative_path}"
    
    return image_url

# Functie om te controleren of een URL bestaat (geen 404)
def url_exists(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Functie om afbeeldingen in de repository te verwerken
def update_readme_with_images():
    readme_path = os.path.join(repo_path, 'README.md')
    
    # Open de README om te lezen
    with open(readme_path, 'r', encoding='utf-8') as file:
        readme_content = file.readlines()
    
    # Maak een lijst van alle afbeeldingen in je repository
    image_files = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):  # Voeg extra extensies toe als nodig
                image_files.append(os.path.join(root, file))
    
    # Maak een string voor de nieuwe afbeeldingen die toegevoegd moeten worden
    image_urls = ''
    for image_file in image_files:
        image_url = get_raw_url(image_file)  # Haal de juiste GitHub raw URL op
        if url_exists(image_url):  # Controleer of de URL bestaat
            image_urls += f'| ![Image]({image_url}) '  # Voeg de markdown voor elke afbeelding toe
        else:
            print(f"URL bestaat niet: {image_url}")  # Meld als de URL niet bestaat
    
    # Vervang de regel met "Column 1 | Column 2 | Column 3 | Column 4 |" door de nieuwe afbeeldingen
    updated_content = ""
    image_index = 0
    for line in readme_content:
        # Als we de regel met de kolommen vinden, voegen we de afbeeldingen toe
        if "| Column 1 | Column 2 | Column 3 | Column 4 |" in line:
            for i in range(0, len(image_files), 4):  # Voeg maximaal 4 afbeeldingen per regel toe
                row = ''
                for j in range(i, min(i + 4, len(image_files))):
                    image_url = get_raw_url(image_files[j])
                    if url_exists(image_url):  # Controleer of de URL bestaat
                        row += f'| ![Image]({image_url}) '
                    else:
                        print(f"URL bestaat niet: {image_url}")  # Meld als de URL niet bestaat
                updated_content += row + "\n"
        else:
            updated_content += line
    
    # Schrijf de bijgewerkte inhoud naar de README
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

# Uitvoeren van de functie om de README bij te werken
update_readme_with_images()
