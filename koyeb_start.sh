#!/bin/bash

# Télécharger les poids du modèle
python download_weights.py

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Appliquer les migrations
python manage.py migrate

# Démarrer le serveur
gunicorn plate_detection_api.wsgi:application