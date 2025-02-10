# import des librairies
import streamlit as st
import pandas as pd
import os
import csv
import re
import matplotlib.pyplot as plt
#importe des fonctions depuis des modules externes
from modules.yt_qualif_dest import qualif_destination
from modules.groq_poi import trouver_poi
from modules.yt_rech_video_title import recherche_video_title
from modules.connect_yt_api import connect_api_youtube
from modules.gr_tendance_dest import graph_dest_tendance
from modules.nlp import analyze_sentiment, crea_df_ana_sent, clean_text, extract_emotional_words, plot_wordcloud

# ----------------------Partie 0 : Styles --------------------

# definition des styles de la page
page_bg_img = '''
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    background-size: cover;
    background-position: center;
}
.st-emotion-cache-mtjnbi {
    width: 80%;
    max-width:unset;
    margin-right: auto;
    margin-left: auto;
}
.body-text {
    font-size: 2.7rem;
    font-weight:900;
    color:white;
    text-align: center;
    max-width: 80%;
    margin: auto;
}
.st-emotion-cache-ue6h4q {
    color: white;
}
.st-emotion-cache-1104ytp p{
    font-size: 2rem;
}
.st-emotion-cache-1104ytp ul{
    background-color:white;
    padding:25px;
    border-radius:10px;
    font-size:2rem;
}
.st-emotion-cache-1104ytp ol{
    background-color:white;
    padding:25px;
    border-radius:10px;
    font-size:2rem;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# ----------------------Partie 1 : Info lancement streamlit DEBUG--------------------

if "RUN_COUNT" not in st.session_state:
    st.session_state["RUN_COUNT"] = 0

st.session_state["RUN_COUNT"] += 1
print(f"🚀 Streamlit a exécuté ce script {st.session_state['RUN_COUNT']} fois.")

# ----------------------Partie 2 : Vérification Youtube Connecté ----------------------

# Vérifier si l'API YouTube est connectée dans la session
if "youtube" not in st.session_state:
    #on lance la connexion
        connect_api_youtube()  # Initialise et stocke `youtube`
# Si connecté, on récupère l'instance YouTube API
if "youtube" in st.session_state:
    youtube = st.session_state.youtube  

# ----------------------Partie 3 : Vérification dossier datas ----------------------

#on verifie une fois que le dossier datas existe sinon on le crée
os.makedirs("datas", exist_ok=True)


# Titre de la page
st.markdown('<div class="body-text">Tout savoir sur une destination en 10 points</div>', unsafe_allow_html=True)

# ----------------------Partie 4 : Construction de la requete ----------------------

# Liste des mots-clés additionnels
mc_add = ['travel','tourism']   

# zone de saisie de la destination par l'utisateur et elimination des espaces
search_query = st.text_input("Saisir ta destination (ville, pays, région, etc.)").strip()
# Bouton pour lancer la recherche
clic_bouton = st.button(f'Obtenir les infos')  # Bouton pour lancer la recherche

# on ajoute les mots clés additionnels à la recherche avec vérification de la saisie
if search_query:  
    # Création d'une liste contenant chaque mot-clé associé à la destination
    search_keywords = " ".join([f"{search_query} {mc}" for mc in mc_add])
    # Construit la requête finale en ajoutant la destination seule + mots-clés associés
    full_query = f"{search_query} {search_keywords}"
else:
    # Si l'utilisateur n'a rien saisi, la requête est vide
    full_query = ""

# ----------------------Partie 5 : Recherche de la destination ----------------------

# on verifie que la zone est remplie et que le bouton est cliqué (donc validation de la recherche)
if search_query and clic_bouton: 
    # on regarde si la destination n'a pas déjà été recherchée
    sai_destination = f"datas/poi_{search_query.replace(' ', '_').lower()}.csv"
    # si le fichier existe déjà
    if os.path.exists(sai_destination):
        # on charge le fichier local
        poi_destination = pd.read_csv(sai_destination) # on prend le fichier local
        # Affichage du tableau de résultats
        st.table(poi_destination)
        # on affiche le graphique
        #insérer la fonction affichage du graphique ici
    else :
        #on vide le cache pour refaire une recherche
        st.cache_data.clear()
        # on appelle la fonction pour récupérer les données via API YouTube
        df_destination, video_ids = qualif_destination(full_query, search_query)
        # Vérifier si la liste est vide        
        if not video_ids:  
            st.write("Aucune vidéo trouvée pour cette destination.")
            #st.stop()
            print("DEBUG: Colonnes actuelles de df_destination :", df_destination.columns)
        print('On appelle la fonction pour trouver poi llm')
        mes_poi = trouver_poi(search_query)
        # Affichage du tableau de résultats
        st.title("Points d'intérêt détectés")
        st.write(mes_poi)

        # Enregistrement des POI dans un fichier CSV
        poi_csv_filename = f"datas/poi_{search_query.replace(' ', '_').lower()}.csv"
        
        with open(poi_csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            #writer.writerow(["Point d'Intérêt"])  # En-tête
            writer.writerow([mes_poi])  #Met tout le texte en une seule cellule

        print(f"Le fichier '{poi_csv_filename}' a été créé avec succès.")
    
    # ----------------------Partie 6 : Création DF_Title et affichage du graphique ----------------------
        
        #création du dataframe pour le graphique avec title
        print("je fais le df_title")
        df_title = recherche_video_title(full_query, search_query, youtube, max_results=50, besoin_videos=100)
        print("df_title est fait")
        st.title("Intérêt pour la destination")
        # affichage du graphique
        # insérer fonction du graphique
        fig = graph_dest_tendance(df_title)
        st.plotly_chart(fig)
        
        # ----------------------Partie 7 : Analyse de sentiment ----------------------
        
        df_ana_sent = crea_df_ana_sent(df_destination)  # Création du DF pour le sentiment analysis
        df_ana_sent["TranscriptClean"] = df_ana_sent["Transcript"].apply(clean_text)  # Nettoyage
        df_ana_sent["Sentiment Score"] = df_ana_sent["TranscriptClean"].apply(analyze_sentiment)  # Analyse
        
        emotion_words = extract_emotional_words(df_ana_sent["TranscriptClean"])
        # st.write("📊 Mots émotionnels dominants :", emotion_words)
        st.title("Mots Emotionnels dominants")

        # Affichage du nuage de mots
        plot_wordcloud(emotion_words)


        print(df_ana_sent.head())
        print("ci dessous le describe")
        print(df_ana_sent["Sentiment Score"].describe())  # Vérifie min, max, moyenne
        print("echantillon aléatoire")
        print(df_ana_sent.sample(10)[["Transcript", "Sentiment Score"]])

        
        
        
            
        # On sauvegarde les datasets en local
        # poi_destination.to_csv(f"datas/poi_{search_query.replace(' ', '_').lower()}.csv", index=False)
        df_destination.to_csv(f"datas/dest_{search_query.replace(' ', '_').lower()}.csv", index=False)
            
            