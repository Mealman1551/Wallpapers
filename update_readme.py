import os
import requests

# Map van je lokale GitHub repository
repo_path = "d:/Github Git Repo clones/Wallpapers"

# Bestandspad van de README.md
readme_path = os.path.join(repo_path, "README.md")

# Functie om alle afbeeldingsbestanden te vinden in de repository
def find_images_in_repo(repo_path):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    image_paths = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in image_extensions):
                image_paths.append(os.path.join(root, file))
    
    return image_paths

# Functie om de raw URL van een afbeelding te krijgen
def get_raw_url(img_path):
    relative_path = img_path.replace(repo_path + os.sep, '').replace(os.sep, '/')
    image_url = f"https://raw.githubusercontent.com/Mealman1551/Wallpapers/refs/heads/main/{relative_path}"
    
    # Probeer de URL te bereiken en kijk of deze werkt
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            return image_url
        else:
            print(f"URL voor {img_path} geeft een fout {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Fout bij het ophalen van {img_path}: {e}")
        return None

# Functie om de inhoud van de README.md bij te werken
def update_readme_with_images(readme_path, image_urls):
    with open(readme_path, "r", encoding="utf-8") as file:
        readme_content = file.read()

    # Scheid de header van de tabel met afbeeldingen
    header_end = readme_content.find("| Column 1 |")  # Dit is de lijn waar de kolomheader begint
    if header_end == -1:  # Als er geen tabel is, voeg dan de nieuwe afbeeldingen bovenaan
        header_end = len(readme_content)

    before_images_content = readme_content[:header_end]  # Bovenkant behouden
    after_images_content = readme_content[header_end:]  # De rest (waar de afbeeldingen komen) behouden

    # Maak nieuwe kolommen met afbeeldingen
    columns = ['Column 1', 'Column 2', 'Column 3', 'Column 4']
    new_table = "| " + " | ".join(columns) + " |\n| " + " | ".join(['---' for _ in columns]) + " |\n"
    image_counter = 0

    for img_path in image_urls:
        # Vervang spaties door %20 voor geldige URL
        img_path = img_path.replace(' ', '%20')
        
        # Haal de werkende raw URL op
        image_url = get_raw_url(img_path)
        if not image_url:
            continue  # Als de URL niet werkt, ga verder met de volgende afbeelding

        if image_counter % len(columns) == 0 and image_counter != 0:
            new_table += "\n"
        
        new_table += f"| ![Image]({image_url}) "
        image_counter += 1

    # Voeg de nieuwe tabel toe na de header en vóór de rest van de inhoud
    updated_readme_content = before_images_content + new_table + after_images_content

    # Sla de bijgewerkte README op
    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(updated_readme_content)
    print("README.md is bijgewerkt met nieuwe afbeeldingen.")

# Haal alle afbeeldingsbestanden uit de repository
image_files = find_images_in_repo(repo_path)

# Update de README met de nieuwe afbeeldingen
update_readme_with_images(readme_path, image_files)
