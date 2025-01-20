# Historique des versions de poi_analyse.py

## v1 - Basique (Sans parallélisation)
- Traitement séquentiel
- Très lent sur les gros datasets
50 vidéos donc 50 transcripts sans le multiprocessing =  47.78 second sur mexico

## v2 - Basique (vader)
- Optimisation NLP (VADER + nlp.pipe)


## v3 - Multiprocessing
- Ajout de multiprocessing.Pool
- Problèmes de compatibilité avec Streamlit

## v3 - Hybride (Thread + Multiprocessing)
- Utilisation de ThreadPoolExecutor
- Optimisation NLP (VADER + TextBlob)
- Temps réduit à ~1.5s pour 50 POI

🔹 Temps récupération YouTube API : 2.80s
🔹 Temps récupération Transcripts : 7.76s
🔹 Temps ajout Transcripts dataframe : 0.00s
🔹 Temps récupération POI : 0.74s
🔹 Temps affichage POI : 0.02s
