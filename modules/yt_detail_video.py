   

def recup_detail_video_yt(video_ids,youtube):
    """
    Récupère les détails des vidéos via l'API YouTube.
    en partant de la liste des video_ids
    Si on a plus de 50 vidéos à traiter.
    Récupère les détails des vidéos en batchs de 50 max (limite API).
    
    """
    print(f"🛠 Début de recup_detail_video_yt : {len(video_ids)} vidéos à récupérer")
    
    video_details = []  # Liste qui va stocker tous les résultats

    # 🔹 Découper la liste en batchs de 50 vidéos max
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]  # Sélectionne un groupe de 50 vidéos max
        print(f"Envoi du batch {i//50+1} à l'API YouTube : {batch}")

        try:
            response = youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join(batch)  # Transforme le batch en une seule chaîne
            ).execute()

            video_details.extend(response.get('items', []))  # Ajouter les résultats du batch

        except Exception as e:
            print(f"Erreur lors de la récupération des détails : {e}")

    print(f"🛠 Fin de recup_detail_video_yt - {len(video_details)} vidéos récupérées")
    return video_details  # Retourne la liste complète
