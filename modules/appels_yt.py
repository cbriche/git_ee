from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import isodate
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


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

# Fonction pour qualifier une destination via YouTube (benédicte)
def qualif_destination(search_query):
    """
    Recherche des vidéos YouTube sur une destination et retourne un DataFrame Pandas.
    """
    # Calculer la date limite pour les 10 dernières années
    date_limit = (datetime.now() - timedelta(days=10 * 365)).isoformat("T") + "Z"

    # Initialiser une liste pour stocker les résultats
    video_data = []

    # Paramètres pour la pagination
    max_results_per_page = 50  # 50 est le Maximum permis par l'API
    # Nombre de vidéos souhaitées maximum
    total_videos_needed = 20  # Nombre total de vidéos souhaitées
    next_page_token = None

    try:
        # Étape 1 : Effectuer des recherches paginées et collecter les données
        while True:
            # Requête de recherche
            search_response = youtube.search().list(
                part='snippet',
                q=search_query,
                type='video',
                maxResults=max_results_per_page,
                #gl="US",  # Résultats localisés aux États-Unis
                regionCode="US",  # Cible les vidéos des États-Unis
                relevanceLanguage = "en",  # Langue anglaise
                publishedAfter=date_limit,  # Vidéos publiées au cours des 10 dernières années
                pageToken=next_page_token
            ).execute()

            # on remplace la boucle for par une liste en compréhension, plus rapide 
            # qui permet de récupérer les videoId et de les stocker dans une liste
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            # on gere le doublon eventuel on transforme la liste en set puis on la remet en liste
            video_ids = list(set(video_ids))
            
            # Aucune vidéo trouvée, on arrête la recherche
            if not video_ids:
                break  
            
            # Étape 2 : Récupération des détails des vidéos en une seule requête (optimisation)
            video_response = youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join(video_ids)  # Convertir la liste en une chaîne séparée par des virgules
            ).execute()           
            
            for video in video_response.get('items', []):   
                # Récupérer les détails de chaque vidéo
                snippet = video.get('snippet', {})
                statistics = video.get('statistics', {})
                content_details = video.get('contentDetails', {})

                # Durée (convertie en secondes pour comparaison)
                raw_duration = content_details.get('duration', 'PT0S')
                duration_seconds = int(isodate.parse_duration(raw_duration).total_seconds())

                # Critères de filtre
                if (int(statistics.get('viewCount', 0)) >= 1000 and
                        int(statistics.get('commentCount', 0)) >= 20 and
                        240 <= duration_seconds <= 1200):  # 4 minutes à 20 minutes
                    # Ajouter les données filtrées dans la liste
                    video_data.append({
                        'Video_ID': video['id'],
                        'Title': snippet.get('title', 'Non disponible'),
                        'Description': snippet.get('description', 'Non disponible'),
                        'Published At': snippet.get('publishedAt', 'Non disponible'),
                        'Duration (Seconds)': duration_seconds,
                        'View Count': statistics.get('viewCount', 0),
                        'Like Count': statistics.get('likeCount', 0),
                        'Comment Count': statistics.get('commentCount', 0),
                        'URL': f"https://www.youtube.com/watch?v={video['id']}",
                        'Channel ID': snippet.get('channelId'),
                    })
                    if len(video_data) >= total_videos_needed:
                        break  # Stopper la boucle dès qu'on a le nombre requis

            # Préparer la page suivante a condition que nous n'avons pas atteint 
            # le nombre total de vidéos souhaitées
            if len(video_data) >= total_videos_needed or 'nextPageToken' not in search_response:
                break  # Sortir de la boucle si on a assez de vidéos ou plus de pages

            # Mettre à jour le token pour la prochaine page (si disponible)
            next_page_token = search_response.get('nextPageToken')

            # Vérifier si la page suivante existe bien
            if not next_page_token:
                break  # Plus de pages disponibles, on arrête la recherche

    except Exception as e:
        print(f"Erreur lors de l'appel à l'API YouTube : {e}")
        # Retourne un DataFrame vide en cas d'erreur et une liste portant les video_ids
        return pd.DataFrame(), []  

    # Étape 3 : Convertir les résultats en DataFrame Pandas
    df_destination = pd.DataFrame(video_data)
    
    # Retourner le DataFrame et la liste des identifiants des vidéos    
    return df_destination, video_ids

# fonction de récupération des transcripts youtube (mireille)
def recup_transcript(video_ids):
    #création d'un dictionnaire pour stocker les transcripts
    transcripts = {}
    #boucle pour récupérer les transcripts de chaque vidéo dans videos_ids
    for video_id in video_ids:
        try:
            #récupération du transcript d'une vidéo, retourne une liste de dictionnaires
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            #on transforme la liste de dictionnaires en texte et on l'ajoute au dictionnaire transcripts
            # avec video_id comme clé
            transcripts[video_id] = " ".join([entry['text'] for entry in transcript])
        except Exception as e:
            #en cas d'erreur, on stocke le message d'erreur dans le dictionnaire (facilera le nettoyage)
            #on limite le retour de l'erreur à 100 caractères
            transcripts[video_id] = f"Transcript non disponible : {str(e)[:100]}..."
    # Retourne tous les transcripts après avoir parcouru toutes les vidéos
    return transcripts  






# Ce bloc de code permet d'éviter que le script soit exécuté automatiquement lorsqu'il est 
# importé dans un autre fichier.
# Il ne s'exécute que si ce fichier est exécuté directement via `python recup_url_yt.py`.
if __name__ == "__main__":
    print("🔹 Test en mode standalone : ce script est exécuté directement.")
