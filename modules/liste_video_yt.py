from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import isodate
from datetime import datetime, timedelta
from modules.connect_yt_api import connect_api_youtube
from dotenv import load_dotenv
import concurrent.futures

# Configuration des paramètres globaux
TOTAL_VIDEOS_NEEDED = 50  # Nombre total de vidéos finales souhaitées

# Calcul du nombre de résultats par page en respectant la limite de l'API YouTube (max = 50)
MAX_RESULTS_PER_PAGE = min(TOTAL_VIDEOS_NEEDED * 2, 50)

#lance la connexion à l'API youtube via la fonction connect_api_youtube
youtube = connect_api_youtube()

# Fonction recherche vidéo 
def recherche_video_yt(full_query):
    """
    Recherche des vidéos YouTube sur une destination et retourne un DataFrame Pandas.
    """
    video_ids = []  # Initialiser une liste pour stocker les identifiants des vidéos
    next_page_token = None
     
    while True:
        try:
            # Étape 1 : Effectuer des recherches paginées et collecter les données
            # Requête de recherche
            search_response = youtube.search().list(
                part='snippet',
                q=full_query, #on fait la requete avec tous les mots clefs (destination + mots clés)
                type='video',
                maxResults=MAX_RESULTS_PER_PAGE,
                order='viewCount',  # Trier par nombre de vues
                videoDuration="medium",  # Filtrer directement les vidéos entre 4 et 20 minutes
                regionCode="US",  # Cible les vidéos des États-Unis
                relevanceLanguage = "en",  # Langue anglaise
                publishedAfter=(datetime.now() - timedelta(days=10 * 365)).isoformat("T") + "Z", # Vidéos publiées au cours des 10 dernières années
                # Évite les vidéos trop récentes qui sont souvent sponsorisées ou boostées artificiellement.
                publishedBefore = (datetime.now() - timedelta(days=30)).isoformat("T") + "Z",  # Exclure les vidéos des 30 derniers jours
                topicId='/m/07bxq', # Topic : Tourisme
                videoCategoryId="19",  # Catégorie : Voyage et événements
                safeSearch="strict", # Filtre le contenu (sexe, violence, discours haineux, etc.).
                # Pagination, si nous avons une autre page à traiter, si pas de next_page_token, on sort de la boucle
                pageToken=next_page_token if next_page_token else None 
            ).execute()
            
            # on remplace la boucle for par une liste en compréhension, plus rapide 
            # qui permet de récupérer les videoId et de les stocker dans une liste
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            # on gere le doublon eventuel on transforme la liste en set puis on la remet en liste
            video_ids = list(set(video_ids))
            
            if 'nextPageToken' in search_response:
                next_page_token = search_response['nextPageToken']
            else:
                break  
            
                      
        except Exception as e:
            print(f"Erreur lors de l'appel à l'API YouTube : {e}")
            # Retourne un DataFrame vide en cas d'erreur et une liste portant les video_ids
            return []
    # on retourne la liste des video_ids 
    if not video_ids:  # Vérifie si la liste est vide
        print("Aucune vidéo trouvée pour cette destination.")
        return []
    else:   
        return video_ids

def recup_detail_video_yt(video_ids):
    """
    Récupère les détails des vidéos via l'API YouTube.
    en partant de la liste des video_ids
    """
    # Étape 2 : Récupération des détails des vidéos en une seule requête (optimisation)
    video_response = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=','.join(video_ids)  # Convertir la liste des videosId en une chaîne séparée par des virgules
        ).execute() 
    return video_response.get('items', [])

def filtrer_video_yt(videos, min_views=1000, min_comments=20):
    """
    Filtre les vidéos selon les critères définis.
    """
    # Initialiser une liste pour stocker les résultats
    video_data = []
    
    #boucle pour récupére les détails de chaque vidéo
    for video in videos:
        # Récupérer les détails de chaque vidéo
        snippet = video.get('snippet', {})
        statistics = video.get('statistics', {})
        content_details = video.get('contentDetails', {})
        
        # Durée (convertie en secondes pour comparaison)
        raw_duration = content_details.get('duration', 'PT0S')
        duration_seconds = int(isodate.parse_duration(raw_duration).total_seconds())

        # Critères de filtre
        if (int(statistics.get('viewCount', 0)) >= min_views and
            int(statistics.get('commentCount', 0)) >= min_comments):
            
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
            
    return video_data
   
# Fonction pour qualifier une destination via YouTube (benédicte)
def qualif_destination(full_query):
    """
    Recherche des vidéos YouTube sur une destination et retourne un DataFrame Pandas.
    """
    # on génére la liste des video_ids
    video_ids = recherche_video_yt(full_query)
    
    # si la liste des vidéos ID est vide on retourne un DataFrame vide
    if not video_ids:
        return pd.DataFrame(), []
    
    
    # on récupère les détails des vidéos
    videos = recup_detail_video_yt(video_ids)
        
    # on filtre les vidéos selon les critères définis
    videos_filtres = filtrer_video_yt(videos)
    
    # on retourne un DataFrame Pandas et la liste des video_ids
    df_destination = pd.DataFrame(videos_filtres[:TOTAL_VIDEOS_NEEDED])
    
    return df_destination, video_ids
    
# Ce bloc de code permet d'éviter que le script soit exécuté automatiquement lorsqu'il est 
# importé dans un autre fichier.
# Il ne s'exécute que si ce fichier est exécuté directement via `python liste_video_yt.py`.
if __name__ == "__main__":
    print("🔹 Test en mode standalone : ce script est exécuté directement.")