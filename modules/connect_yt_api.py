from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os

def connect_api_youtube():
    # Charger les variables d'environnement (clé API)
    load_dotenv()

    # Gestion de la clé API YouTube
    API_KEY = os.getenv("YOUTUBE_API_KEY") # .env
    print(f"Clé API chargée : {API_KEY}")  # DEBUG : Vérifier la clé API
    # Vérifier si la clé API est bien chargée
    if not API_KEY:
        # raise interrompt tout le programme si il y a une erreur.
        raise ValueError("Erreur : La clé API YouTube n'est pas définie. Vérifie ton fichier .env.")

    # Créer le service API (à faire une seule fois)
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    return youtube

# Cette partie empêche l'exécution automatique lors de l'import
if __name__ == "__main__":
    print("🔹 Test : connexion à l'API YouTube")
    youtube = connect_api_youtube()
    print("🔹 Connexion réussie")