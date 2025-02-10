# Fonction recherche vidéo 
import pandas as pd
import streamlit as st
from modules.connect_yt_api import connect_api_youtube



# Fonction recherche vidéo
def recherche_video_title(full_query, search_query, youtube, max_results, besoin_videos):
    """
    Recherche des vidéos YouTube sur une période donnée et retourne un DataFrame avec Année et Titre.
    """
    video_data = []  # Stocke les résultats (année, titre)
    next_page_token = None

    while True:
        try:
            # Appel API YouTube
            search_response = youtube.search().list(
                part='snippet',
                q=full_query,
                type='video',
                maxResults=max_results,
                regionCode="FR",
                relevanceLanguage="fr",
                publishedAfter="2014-01-01T00:00:00Z",  # Début période
                publishedBefore="2024-12-31T23:59:59Z",  # Fin période
                pageToken=next_page_token if next_page_token else None
            ).execute()
            
            # Filtrer les vidéos contenant la requête dans le titre
            for item in search_response.get("items", []):
                title = item["snippet"]["title"]
                published_at = item["snippet"]["publishedAt"][:4]  # Récupérer l'année
                if search_query.lower() in title.lower():
                    video_data.append((published_at, title))

            # Suppression des doublons
            video_data = list(set(video_data))

            # Arrêt si on a atteint le nombre demandé
            if len(video_data) >= besoin_videos:
                break

            # Vérification de la pagination
            next_page_token = search_response.get('nextPageToken')
            if not next_page_token:
                break  

        except Exception as e:
            st.error(f"Erreur API YouTube : {e}")
            return pd.DataFrame(columns=["Année", "Titre"])  # Retourne un DataFrame vide en cas d'erreur
        
    # Création du DataFrame
    df_title = pd.DataFrame(video_data, columns=["Année", "Titre"])
    # sauvegarde le dataframe
    df_title.to_csv(f"datas/title_{search_query.replace(' ', '_').lower()}.csv", index=False)         

    # retourne df_title
    return df_title



    