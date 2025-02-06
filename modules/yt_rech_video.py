

# Fonction recherche vidéo 
def recherche_video_yt(full_query,search_query,youtube,max_results,besoin_videos):
    """
    Recherche des vidéos YouTube sur une destination et retourne un DataFrame Pandas.
    """
    video_ids = []  # Initialiser une liste pour stocker les identifiants des vidéos filtrées sur le title
    next_page_token = None
    while True:
        try:
            # Étape 1 : Effectuer des recherches paginées et collecter les données
            # Critère de recherche
            search_response = youtube.search().list(
                part='snippet',
                q=full_query, #on fait la requete avec tous les mots clefs (destination + mots clés)
                type='video',
                maxResults=max_results,
                # order='viewCount',  # Trier par nombre de vues
                # videoDuration="medium",  # Filtrer directement les vidéos entre 4 et 20 minutes
                regionCode="FR",  # Cible les vidéos des États-Unis
                relevanceLanguage = "fr",  # Langue anglaise
                # publishedAfter=(datetime.now() - timedelta(days=10 * 365)).isoformat("T") + "Z", # Vidéos publiées au cours des 10 dernières années
                # # Évite les vidéos trop récentes qui sont souvent sponsorisées ou boostées artificiellement.
                # publishedBefore = (datetime.now() - timedelta(days=30)).isoformat("T") + "Z",  # Exclure les vidéos des 30 derniers jours
                #topicId='/m/07bxq', # Topic : Tourisme
                #videoCategoryId="19",  # Catégorie : Voyage et événements
                #safeSearch="strict", # Filtre le contenu (sexe, violence, discours haineux, etc.).
                # Pagination, si nous avons une autre page à traiter, si pas de next_page_token, on sort de la boucle
                pageToken=next_page_token if next_page_token else None 
            ).execute()
                   
            # Filtrer les vidéos contenant le search_query dans le titre (mot saisi par l'utilisateur)
            filtered_videos = [
                (item["id"]["videoId"], item["snippet"]["title"])
                for item in search_response.get("items", [])
                if search_query.lower() in item["snippet"]["title"].lower()
            ]
            
            # on ajoute les vidéos filtrées à la liste des video_ids
            video_ids.extend(filtered_videos)

            
            # on gere le doublon eventuel on transforme la liste en set puis on la remet en liste
            video_ids = list(set(video_ids))
            
             # 🔥 Ajout de l'optimisation : arrêter la pagination si on a assez de vidéos
            if len(video_ids) >= besoin_videos:
                print(f"✅ {besoin_videos} vidéos atteintes, arrêt de la pagination.")
                break  # On arrête la boucle dès qu'on a assez de vidéos
            
                        
            # Vérifier s'il y a une page suivante
            print(f"on vérifie s'il y a une page suivante")
            if 'nextPageToken' in search_response:
                next_page_token = search_response['nextPageToken']
            else:
                break  
            
                      
        except Exception as e:
            print(f"Erreur lors de l'appel à l'API YouTube : {e}")
            # Retourne une liste vide en cas d'erreur
            return []
        
     # Vérifier si on a bien récupéré des vidéos
    if not video_ids: 
        print("Aucune vidéo valide trouvée après filtrage title.")
        return []
    else:
        # on récupére uniquement l'ID des vidéos
        video_ids = [vid[0] if isinstance(vid, tuple) else vid for vid in video_ids]  # Extraction propre des IDs
        # on renvoie la liste des vidéos
        return video_ids
    

# Ce bloc de code permet d'éviter que le script soit exécuté automatiquement lorsqu'il est 
# importé dans un autre fichier.
# Il ne s'exécute que si ce fichier est exécuté directement via `python liste_video_yt.py`.
if __name__ == "__main__":
    print("🔹 Test en mode standalone : ce script est exécuté directement.")


    