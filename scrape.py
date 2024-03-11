import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

def scrape_google_images(query, num_images, df, type, number, folder="dataset"):
    name = query.replace(" ", "_")
    # URL de recherche Google Images
    url = f"https://www.google.com/search?q={query}&tbm=isch"

    # Headers de l'utilisateur pour simuler un navigateur
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Envoi de la requête HTTP
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Création d'un dossier pour stocker les images
    if not os.path.exists(os.path.join(folder, name.replace(" ", "_"))):
        os.makedirs(os.path.join(folder, name.replace(" ", "_")))

    # Extraction des liens des images et téléchargement
    image_links = soup.find_all("img")
    print(f"{len(image_links)} images")
    for i, image_link in enumerate(image_links[:num_images]):
        image_url = image_link.get("src")
        if image_url:
            if image_url.startswith("http"):
                image_name = os.path.join(folder, name, f"{name}_{i}.jpg")
                with open(image_name, "wb") as f:
                    f.write(requests.get(image_url).content)
                df.loc[len(df)] = [image_name, type, number]
                print(f"Image {i+1} téléchargée avec succès")

card_type = ["spades", "hearts", "diamonds", "clubs"]
card_number = ["seven", "eight", "nine", "ten", "jack", "queen", "king", "ace"]

df = pd.DataFrame(columns=["number", "type", "path"])

for t in card_type:
    for n in card_number:
        scrape_google_images(f"{n} of {t} card", 50, df, t, n)

df.to_csv("dataset/dataset.csv")