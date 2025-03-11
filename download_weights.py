#!/usr/bin/env python
"""
Script pour télécharger les fichiers de poids YOLO depuis Google Drive
"""
import os
import requests
import sys
from tqdm import tqdm

def download_file(url, destination):
    """Télécharge un fichier depuis une URL avec barre de progression."""
    if os.path.exists(destination):
        print(f"Le fichier {destination} existe déjà. Téléchargement ignoré.")
        return True
        
    print(f"Téléchargement de {destination}...")
    try:
        # Créer le dossier de destination s'il n'existe pas
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        # Télécharger le fichier
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Taille totale en octets
        total_size = int(response.headers.get('content-length', 0))
        
        # Télécharger avec barre de progression
        with open(destination, 'wb') as file, tqdm(
            desc=os.path.basename(destination),
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                size = file.write(chunk)
                bar.update(size)
        
        print(f"Téléchargement terminé: {destination}")
        return True
    except Exception as e:
        print(f"Erreur lors du téléchargement de {destination}: {e}")
        return False

def main():
    """Fonction principale."""
    # Fichiers à télécharger (remplacez les IDs par les vôtres)
    files_to_download = {
        "weights/detection/yolov3-detection_final.weights": "https://drive.google.com/uc?export=download&id=1MYHSar4I_CpCsZA6iF0DEBIMGAgmqQNF",
        "weights/ocr/yolov3-ocr_final.weights": "https://drive.google.com/uc?export=download&id=10spTQpaad51AZy64RLX45-TCABwq_Uxt",
    }

    # Créer les dossiers de poids s'ils n'existent pas
    os.makedirs("weights/detection", exist_ok=True)
    os.makedirs("weights/ocr", exist_ok=True)

    # Télécharger tous les fichiers
    success = True
    for path, url in files_to_download.items():
        if not download_file(url, path):
            success = False

    if success:
        print("✅ Tous les fichiers de poids ont été téléchargés avec succès!")
        return 0
    else:
        print("❌ Certains fichiers n'ont pas pu être téléchargés.")
        return 1

if __name__ == "__main__":
    sys.exit(main())