import os
import glob
import requests

# Pad naar je lokale GitHub repository
repo_path = r"D:\Github Git Repo clones\Wallpapers"

# Pad naar de README.md bestand
readme_path = os.path.join(repo_path, 'README.md')

# Functie om alle afbeeldingen in je repository te verzamelen
def get_image_files():
    image_files = []
    # Zoek naar alle afbeeldingsbestanden (jpeg, png, jpg, etc.)
    for ext in ('*.jpeg', '*.jpg', '*.png', '*.gif'):
        image_files.extend(glob.glob(os.path.join(repo_path, '**', ext), recursive=True))
    return image_files

# Functie om de afbeelding URL's te genereren
def generate_image_urls(image_files):
    urls = []
    for image_file in image_files:
        # Zorg dat spaties in de paden worden omgezet naar %20 voor de URL
        url_path = image_file.replace(repo_path, '').replace(os.sep, '/').lstrip('/')
        url_path = url_path.replace(' ', '%20')  # Vervang spaties door %20
        url = f"https://raw.githubusercontent.com/Mealman1551/Wallpapers/refs/heads/main/{url_path}"
        urls.append(url)
    return urls

# Functie om de content van de README.md te lezen
def read_readme():
    with open(readme_path, 'r', encoding='utf-8') as file:
        return file.readlines()

# Functie om de gewijzigde inhoud weer naar de README.md te schrijven
def update_readme(content):
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.writelines(content)

# Functie om de README.md volledig bij te werken met de nieuwe afbeeldingen
def update_readme_with_images():
    # Lees de bestaande inhoud van de README (hoeft niet meer, we gaan de inhoud overschrijven)
    # Lees de afbeeldingen op uit de repository
    image_files = get_image_files()

    # Genereer de URL's voor de afbeeldingen
    image_urls = generate_image_urls(image_files)

    # Maak een nieuwe sectie voor de afbeeldingen in de kolommen
    columns = "| Wallpapers |\n|---------|\n"
    rows = []
    for i in range(0, len(image_urls), 1):  # 1 afbeelding per rij (centrale kolom)
        row = f"![Image]({image_urls[i]})"
        rows.append(f"{row} |\n")

    # Tekst die bovenaan moet blijven
    top_text = """# Meal's Wallpaper collection

## Copyright

### AI Generated

Free to use without mentioning me or the AI I used.

### I found

Free to use without mentioning me, however the images come from sites like: Unsplash, Pixabay, Flickr, Windows Spotlight, Pexels and more, some images requires mentioning of the official creator (idk what images or who but yea...)

### Selfmade

Free to use but please, please, for the sake of god, mention me, Mealman1551.

### What if Selfmade images are not mentioned with my name (Mealman1551)?

I don't make a lawsuit of it, but I'm the original creator so yea... Be decent and do me a favor and mention me as "Mealman1551".

## Updates

The wallpapers are updated regularly.

###### © 2025 Mealman1551
"""

    # Combineer de top tekst en de nieuwe afbeelding kolom
    updated_content = [top_text] + [columns] + rows

    # Werk de README bij met de nieuwe inhoud (dit overschrijft de oude inhoud)
    update_readme(updated_content)

# Voer de update uit
update_readme_with_images()
print("README.md is volledig bijgewerkt met de nieuwste afbeeldingen!")
