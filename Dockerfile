FROM python:3.10-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p media/uploads media/results media/tmp weights/detection weights/ocr

# Créer et rendre le script de démarrage exécutable
RUN echo '#!/bin/bash\n\n# Télécharger les poids du modèle\npython download_weights.py\n\n# Collecter les fichiers statiques\npython manage.py collectstatic --noinput\n\n# Appliquer les migrations\npython manage.py migrate\n\n# Démarrer le serveur\ngunicorn plate_detection_api.wsgi:application --bind=0.0.0.0:8000' > koyeb_start.sh && \
    chmod +x koyeb_start.sh

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["./koyeb_start.sh"]