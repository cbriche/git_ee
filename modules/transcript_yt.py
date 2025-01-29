from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import isodate
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import concurrent.futures

# Charger les variables d'environnement (clé API)
load_dotenv()

# # Gestion de la clé API YouTube
# API_KEY = os.getenv("YOUTUBE_API_KEY") # .env
# print(f"Clé API chargée : {API_KEY}")  # DEBUG : Vérifier la clé API
# # Vérifier si la clé API est bien chargée
# if not API_KEY:
#     # raise interrompt tout le programme si il y a une erreur.
#     raise ValueError("Erreur : La clé API YouTube n'est pas définie. Vérifie ton fichier .env.")

# # Créer le service API (à faire une seule fois)
# youtube = build('youtube', 'v3', developerKey=API_KEY)


# ---------- OPTIMISATION : Récupération des transcripts en parallèle multiprocessing----------

# Fonction pour récupérer le transcript d'1 vidéo
def fetch_transcript(video_id):
    """ Récupère le transcript d'une vidéo donnée """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return video_id, " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        return video_id, f"Transcript non disponible : {str(e)[:100]}..."

def recup_transcript(video_ids, max_workers=15):
    """ Récupère 15 transcripts en parallèle """
    transcripts = {}

    # Utilisation de ThreadPoolExecutor pour paralléliser les requêtes (VikThor)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(fetch_transcript, video_ids)

    # Stockage des résultats dans un dictionnaire
    for video_id, transcript in results:
        transcripts[video_id] = transcript

    return transcripts

# ---------- FIN OPTIMISATION ----------

# Ce bloc de code permet d'éviter que le script soit exécuté automatiquement lorsqu'il est 
# importé dans un autre fichier.
# Il ne s'exécute que si ce fichier est exécuté directement via `python recup_url_yt.py`.
if __name__ == "__main__":
    print("🔹 Test en mode standalone : ce script est exécuté directement.")
