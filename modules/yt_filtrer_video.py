import isodate


def filtrer_video_yt(videos, min_views=1000, min_comments=20):
    """
    Filtre les vidéos selon les critères définis.
    """
    # Initialiser une liste pour stocker les résultats
    videos_filtrees = []
    
    #boucle pour récupére les détails de chaque vidéo de la liste videos
    #récupérer par yt_detail_video.py
    
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
            videos_filtrees.append({
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
            
    return videos_filtrees