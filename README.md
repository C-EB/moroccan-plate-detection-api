# Documentation de l'API de détection de plaques d'immatriculation marocaines

Cette API permet de détecter et reconnaître les plaques d'immatriculation de véhicules marocains à partir d'images. Elle utilise des modèles YOLOv3 personnalisés pour la détection et la reconnaissance de caractères.

## URL de base

```
https://echarif.pythonanywhere.com/api
```

Remplacez `votre-username` par votre nom d'utilisateur PythonAnywhere.

## Authentification

Actuellement, l'API ne nécessite pas d'authentification pour les requêtes.

## Endpoints

### 1. Détecter une plaque d'immatriculation

Détecte une plaque d'immatriculation dans une image et extrait le texte.

**Endpoint:** `/plates/`

**Méthode:** `POST`

**Format de requête:** `multipart/form-data`

**Paramètres:**

| Nom | Type | Requis | Description |
|-----|------|--------|-------------|
| image | File | Oui | Image du véhicule à analyser (formats acceptés: JPG, JPEG, PNG) |
| ocr_method | String | Non | Méthode OCR à utiliser ("trained" ou "tesseract"). Par défaut: "trained" |

**Exemple de requête avec cURL:**

```bash
curl -X POST \
  -F "image=@/chemin/vers/image.jpg" \
  -F "ocr_method=trained" \
  https://votre-username.pythonanywhere.com/api/plates/
```

**Exemple de requête avec Python:**

```python
import requests

url = "https://votre-username.pythonanywhere.com/api/plates/"
files = {"image": open("chemin/vers/image.jpg", "rb")}
data = {"ocr_method": "trained"}

response = requests.post(url, files=files, data=data)
print(response.json())
```

**Exemple de réponse:**

```json
{
  "id": "7e796783-320b-4168-bffc-7bb75b205f1f",
  "image": "/media/uploads/car_image_123.jpg",
  "result_image": "/media/results/car_image_123_result.jpg",
  "plate_text": "666 | 1 | و",
  "confidence": 95.30,
  "created_at": "2025-03-11T10:28:39.123456Z",
  "ocr_method": "trained"
}
```

**Codes de réponse:**

| Code | Description |
|------|-------------|
| 201 | Succès - plaque détectée et texte extrait |
| 400 | Erreur de requête - paramètres manquants ou invalides |
| 500 | Erreur serveur - erreur lors du traitement de l'image |

### 2. Détecter des plaques dans plusieurs images

Détecte des plaques d'immatriculation dans plusieurs images à la fois.

**Endpoint:** `/plates/detect_bulk/`

**Méthode:** `POST`

**Format de requête:** `multipart/form-data`

**Paramètres:**

| Nom | Type | Requis | Description |
|-----|------|--------|-------------|
| images | Files | Oui | Images des véhicules à analyser (formats acceptés: JPG, JPEG, PNG) |
| ocr_method | String | Non | Méthode OCR à utiliser ("trained" ou "tesseract"). Par défaut: "trained" |

**Exemple de requête avec cURL:**

```bash
curl -X POST \
  -F "images=@/chemin/vers/image1.jpg" \
  -F "images=@/chemin/vers/image2.jpg" \
  -F "ocr_method=trained" \
  https://votre-username.pythonanywhere.com/api/plates/detect_bulk/
```

**Exemple de requête avec Python:**

```python
import requests

url = "https://votre-username.pythonanywhere.com/api/plates/detect_bulk/"
files = [
    ("images", open("chemin/vers/image1.jpg", "rb")),
    ("images", open("chemin/vers/image2.jpg", "rb"))
]
data = {"ocr_method": "trained"}

response = requests.post(url, files=files, data=data)
print(response.json())
```

**Exemple de réponse:**

```json
[
  {
    "id": "7e796783-320b-4168-bffc-7bb75b205f1f",
    "image": "/media/uploads/car_image_123.jpg",
    "result_image": "/media/results/car_image_123_result.jpg",
    "plate_text": "666 | 1 | و",
    "confidence": 95.30,
    "created_at": "2025-03-11T10:28:39.123456Z",
    "ocr_method": "trained"
  },
  {
    "id": "8f807894-431c-5279-cgfd-8cc86c316g2g",
    "image": "/media/uploads/car_image_124.jpg",
    "result_image": "/media/results/car_image_124_result.jpg",
    "plate_text": "123 | 4 | أ",
    "confidence": 92.15,
    "created_at": "2025-03-11T10:28:40.789012Z",
    "ocr_method": "trained"
  }
]
```

### 3. Obtenir toutes les détections

Récupère l'historique de toutes les détections effectuées.

**Endpoint:** `/plates/`

**Méthode:** `GET`

**Exemple de requête:**

```bash
curl -X GET https://votre-username.pythonanywhere.com/api/plates/
```

**Exemple de réponse:**

```json
[
  {
    "id": "7e796783-320b-4168-bffc-7bb75b205f1f",
    "image": "/media/uploads/car_image_123.jpg",
    "result_image": "/media/results/car_image_123_result.jpg",
    "plate_text": "666 | 1 | و",
    "confidence": 95.30,
    "created_at": "2025-03-11T10:28:39.123456Z",
    "ocr_method": "trained"
  },
  {
    "id": "8f807894-431c-5279-cgfd-8cc86c316g2g",
    "image": "/media/uploads/car_image_124.jpg",
    "result_image": "/media/results/car_image_124_result.jpg",
    "plate_text": "123 | 4 | أ",
    "confidence": 92.15,
    "created_at": "2025-03-11T10:28:40.789012Z",
    "ocr_method": "trained"
  }
]
```

### 4. Obtenir une détection spécifique

Récupère les détails d'une détection spécifique par son ID.

**Endpoint:** `/plates/{id}/`

**Méthode:** `GET`

**Paramètres de chemin:**

| Nom | Type | Description |
|-----|------|-------------|
| id | String | ID de la détection à récupérer |

**Exemple de requête:**

```bash
curl -X GET https://votre-username.pythonanywhere.com/api/plates/7e796783-320b-4168-bffc-7bb75b205f1f/
```

**Exemple de réponse:**

```json
{
  "id": "7e796783-320b-4168-bffc-7bb75b205f1f",
  "image": "/media/uploads/car_image_123.jpg",
  "result_image": "/media/results/car_image_123_result.jpg",
  "plate_text": "666 | 1 | و",
  "confidence": 95.30,
  "created_at": "2025-03-11T10:28:39.123456Z",
  "ocr_method": "trained"
}
```

## Exemples d'intégration

### Exemple JavaScript (avec fetch)

```javascript
// Fonction pour détecter une plaque d'immatriculation
async function detectPlate(imageFile, ocrMethod = 'trained') {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('ocr_method', ocrMethod);

  try {
    const response = await fetch('https://votre-username.pythonanywhere.com/api/plates/', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Erreur lors de la détection:', error);
    throw error;
  }
}

// Exemple d'utilisation
const fileInput = document.getElementById('plateImage');
fileInput.addEventListener('change', async (event) => {
  const file = event.target.files[0];
  if (file) {
    try {
      const result = await detectPlate(file);
      console.log('Plaque détectée:', result.plate_text);
      console.log('Confiance:', result.confidence + '%');
    } catch (error) {
      console.error('Échec de la détection:', error);
    }
  }
});
```

### Exemple Python (avec requests)

```python
import requests
from PIL import Image
import matplotlib.pyplot as plt
import io

class PlateDetectorClient:
    def __init__(self, base_url="https://votre-username.pythonanywhere.com/api"):
        self.base_url = base_url
        
    def detect_plate(self, image_path, ocr_method="trained"):
        """Détecte une plaque d'immatriculation dans une image"""
        url = f"{self.base_url}/plates/"
        
        with open(image_path, "rb") as img_file:
            files = {"image": img_file}
            data = {"ocr_method": ocr_method}
            
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()  # Lève une exception en cas d'erreur HTTP
            
            return response.json()
    
    def display_result(self, result):
        """Affiche le résultat de la détection"""
        # Télécharger et afficher l'image originale
        orig_img_url = f"{self.base_url}{result['image']}"
        result_img_url = f"{self.base_url}{result['result_image']}"
        
        orig_img_response = requests.get(orig_img_url)
        result_img_response = requests.get(result_img_url)
        
        orig_img = Image.open(io.BytesIO(orig_img_response.content))
        result_img = Image.open(io.BytesIO(result_img_response.content))
        
        # Afficher les images
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        ax1.imshow(orig_img)
        ax1.set_title("Image originale")
        ax1.axis("off")
        
        ax2.imshow(result_img)
        ax2.set_title(f"Plaque détectée: {result['plate_text']}")
        ax2.axis("off")
        
        plt.tight_layout()
        plt.show()
        
        # Afficher les détails
        print(f"Texte de la plaque: {result['plate_text']}")
        print(f"Niveau de confiance: {result['confidence']}%")
        print(f"Méthode OCR: {result['ocr_method']}")
        print(f"ID de détection: {result['id']}")

# Exemple d'utilisation
if __name__ == "__main__":
    client = PlateDetectorClient()
    result = client.detect_plate("chemin/vers/image.jpg")
    client.display_result(result)
```

## Notes d'utilisation

1. **Formats d'image supportés**:
   - JPEG/JPG
   - PNG
   - BMP

2. **Taille d'image optimale**:
   - Pour de meilleurs résultats, utilisez des images avec une résolution minimale de 800x600 pixels
   - La taille maximale d'upload est de 10 MB

3. **Méthodes OCR**:
   - `trained`: Utilise un modèle YOLOv3 personnalisé, optimisé pour les plaques marocaines avec support des caractères arabes
   - `tesseract`: Utilise Tesseract OCR, meilleur pour les caractères latins et les chiffres

4. **Limitations du plan gratuit**:
   - Limite de 100 requêtes par jour
   - Taille maximale de l'image: 10 MB
   - Temps de réponse plus lent pendant les périodes de forte utilisation

## Codes d'erreur communs

| Code | Description | Solution possible |
|------|-------------|-------------------|
| 400 | Fichier d'image manquant | Assurez-vous d'envoyer une image valide dans le champ 'image' |
| 415 | Format de fichier non supporté | Utilisez uniquement JPG, JPEG, PNG ou BMP |
| 413 | Fichier trop volumineux | Redimensionnez l'image à moins de 10 MB |
| 500 | Erreur serveur interne | Réessayez plus tard ou contactez l'administrateur |

