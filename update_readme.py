import os
import re
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

# Functie om de inhoud van de README.md bij te werken
def update_readme_with_images(readme_path, image_urls):
    with open(readme_path, "r", encoding="utf-8") as file:
        readme_content = file.read()
    
    # Zoek de bestaande afbeeldingen en vervang deze
    image_table_pattern = r"(\|.*\|(?:\n|\r\n)*)"
    current_images = re.findall(image_table_pattern, readme_content)
    
    # Maak nieuwe kolommen met afbeeldingen
    columns = ['Column 1', 'Column 2', 'Column 3', 'Column 4']
    new_table = "| " + " | ".join(columns) + " |\n| " + " | ".join(['---' for _ in columns]) + " |\n"
    image_counter = 0

    for img_path in image_urls:
        # Vervang spaties door %20 voor geldige URL
        img_path = img_path.replace(' ', '%20')
        image_url = f"https://raw.githubusercontent.com/mealman1551/wallpapers/main/{img_path.replace(repo_path + os.sep, '').replace(os.sep, '/')}"

        if image_counter % len(columns) == 0 and image_counter != 0:
            new_table += "\n"
        
        new_table += f"| ![Image]({image_url}) "
        image_counter += 1

    # Plaats de nieuwe afbeeldingen bovenaan de README, onder de bestaande tekst
    before_images_content = readme_content.split('| Column 1 |')[0]  # Neem de tekst boven de afbeeldingstabel
    updated_readme_content = before_images_content + new_table + '\n' + ''.join(current_images[1:])  # Voeg de nieuwe tabel toe

    # Sla de bijgewerkte README op
    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(updated_readme_content)
    print("README.md is bijgewerkt met nieuwe afbeeldingen.")

# Haal alle afbeeldingsbestanden uit de repository
image_files = find_images_in_repo(repo_path)

# Update de README met de nieuwe afbeeldingen
update_readme_with_images(readme_path, image_files)
