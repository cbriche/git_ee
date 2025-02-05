import streamlit as st
import pandas as pd
# import des fonctions dans modules
from modules.connect_yt_api import connect_api_youtube
from modules.yt_transcript_video import recup_transcript
from modules.yt_rech_video import recherche_video_yt
from modules.yt_detail_video import recup_detail_video_yt
from modules.yt_filtrer_video import filtrer_video_yt


# Configuration des paramètres globaux
TOTAL_VIDEOS_NEEDED = 5  # Nombre total de vidéos finales souhaitées

# Calcul du nombre de résultats par page en respectant la limite de l'API YouTube (max = 50)
MAX_RESULTS_PER_PAGE = min(TOTAL_VIDEOS_NEEDED * 2, 50)

#lance la connexion à l'API youtube via la fonction connect_api_youtube
youtube = connect_api_youtube()

  
   
# Fonction pour qualifier une destination via YouTube (benédicte)
def qualif_destination(full_query, search_query):
    """
    Recherche des vidéos YouTube, applique plusieurs filtres et retourne un DataFrame final.
    Si on n’a pas 50 vidéos valides, on relance la recherche jusqu'à atteindre le quota.
    """
    print("🔵 Début de qualif_destination()")
    # Stocke les IDs des vidéos déjà testées
    video_ids = set()
    # DataFrame pour stocker les vidéos valide
    df_destination  = pd.DataFrame()  
    
    #tant que le nombre de vidéos est inférieur à TOTAL_VIDEOS_NEEDED, on continue la recherche
    while len(df_destination) < TOTAL_VIDEOS_NEEDED:
        # On initialise `new_video_ids` à une liste vide AVANT de l'utiliser
        new_video_ids = []
        # Étape 1 : dans la liste new_video_ids on récupère les vidéos filtrées sur la requete et le title (fx recherche_video_yt)
        new_video_ids = recherche_video_yt(full_query,search_query,youtube,MAX_RESULTS_PER_PAGE,TOTAL_VIDEOS_NEEDED)
        
        #Si l'API retourne None à cause d'un quota dépassé
        # Ce bloc empêche l’exécution si l’API ne répond plus
        if not new_video_ids:
            st.error("Erreur : L'API YouTube a retourné None (quota dépassé ?)")
            st.stop()  # Arrête immédiatement l'exécution du script Streamlit
            print("⛔️ Cette ligne ne devrait pas être atteinte si `st.stop()` fonctionne !")

        # il est possible que nous récupérions des vidéos déjà traitées
        # Nous devons les retirer de la liste pour éviter les doublons
        new_video_ids = [vid for vid in new_video_ids if vid not in video_ids]
    
        # si la liste des vidéos ID est vide on retourne un DataFrame vide
        # ce bloc empêche l’API de tourner en boucle sur des vidéos déjà récupérées
        if not new_video_ids:
            print(f"Plus de vidéos disponibles après {len(df_destination)} vidéos valides")
            return df_destination, list(video_ids)  # 🔹 Retourne immédiatement un tuple valide
        else:
            # Mettre à jour la liste des vidéos déjà traitées
            # Convertir en set pour supprimer les doublons et utiliser update()
            video_ids = set(video_ids)  
            # Ajouter les nouveaux IDs
            video_ids.update(new_video_ids)  
            # Reconvertir en liste si nécessaire
            video_ids = list(set(video_ids)) 
    
        # Étape 2 : Récupération des détails des vidéos
        videos = recup_detail_video_yt(video_ids,youtube)
        
        if not videos:
            print("Aucune vidéo valide après récupération des détails.")
            return pd.DataFrame(), []
            
        # Étape 3 : Filtrage des vidéos (durée, vues, etc.)
        videos_filtrees = filtrer_video_yt(videos)
        
        if not videos_filtrees:
            print("Toutes les vidéos ont été rejetées après filtrage.(durée, vues, etc.)")
            return pd.DataFrame(), []
        
        # Étape 4 : Vérification de la présence d'un transcript dans les vidéos filtrées par (durée, vues, etc.)"
        transcripts = recup_transcript([video["Video_ID"] for video in videos_filtrees])
        
        # Filtrer les vidéos pour ne garder que celles qui ont un transcript valide
        videos_filtrees = [
            video for video in videos_filtrees 
            if video["Video_ID"] in transcripts and "Transcript non disponible" not in transcripts[video["Video_ID"]]
        ]
        
        # Ajout du transcript au DataFrame
        for video in videos_filtrees:
         video["Transcript"] = transcripts.get(video["Video_ID"], "Transcript non disponible")
        
        if not videos_filtrees:
            print("Aucune vidéo avec transcript disponible.")
            continue
        
        # Étape 5 : Retourner le DataFrame final
        # Ajouter les nouvelles vidéos au DataFrame final
        df_new = pd.DataFrame(videos_filtrees)
        df_destination = pd.concat([df_destination, df_new], ignore_index=True)
        
        # 🔹 Vérification finale avant retour
        if df_destination.empty:
            print("Aucun résultat trouvé, retour d'un DataFrame vide et une liste vide.")
            return pd.DataFrame(), []  # Retourne bien deux valeurs par défaut
             
        print("🔍 Fin de qualif_destination() - df_destination:", df_destination.shape, "- video_ids:", len(video_ids))
        
        if not isinstance(df_destination, pd.DataFrame) or not isinstance(video_ids, list):
            print("❌ Erreur : qualif_destination() retourne un mauvais format :", type(df_destination), type(video_ids))
            return pd.DataFrame(), []
        
        return df_destination, video_ids
    
# Ce bloc de code permet d'éviter que le script soit exécuté automatiquement lorsqu'il est 
# importé dans un autre fichier.
# Il ne s'exécute que si ce fichier est exécuté directement via `python liste_video_yt.py`.
if __name__ == "__main__":
    print("🔹 Test en mode standalone : ce script est exécuté directement.")