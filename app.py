# page stremlit
import streamlit as st
import pandas as pd
import os
from modules.appels_yt import qualif_destination, recup_transcript # Import de la fonction depuis le module externe
from modules.poi_analyse import top_10_poi # Import de la fonction depuis le module externe

#on verifie une fois que le dossier datas existe
os.makedirs("datas", exist_ok=True)

# titre de la page
st.title("Recherche de vidéos YouTube")

# saisie de la destination
search_query = st.text_input("Saisir ta destination (ville, pays, région, etc.)")
clic_bouton = st.button(f'Obtenir les infos')  # Bouton pour lancer la recherche


# on verifie que la zone est remplie et que le bouton est cliqué (donc validation de la recherche)
if search_query and clic_bouton:  # Équivaut à if search_query != ""
    # on regarde si la destination n'a pas déjà été recherchée
    sai_destination = f"datas/poi_{search_query.replace(' ', '_').lower()}.csv"
    # si le fichier existe déjà
    if os.path.exists(sai_destination):
        # on charge le fichier local
        df_destination = pd.read_csv(sai_destination) # on prend le fichier local
        st.write("Résultats 'local' des POI :")
        st.table(df_destination)
    else :
        #on vide le cache pour refaire une recherche
        st.cache_data.clear()
        # on appelle la fonction pour récupérer les données via API YouTube
        df_destination, video_ids = qualif_destination(search_query)
        # on lance la fonction de récupération des transcripts
        transcripts = recup_transcript(video_ids)
        
        # Ajouter les transcriptions au DataFrame
        df_destination["Transcript"] = df_destination["Video_ID"].map(transcripts)
        
        # Sauvegarder les données mises à jour dans le fichier CSV
        #df_destination.to_csv(sai_destination, index=False)
    
        # on appelle la fonction pour récupérer les points d'intérêt
        poi_destination = top_10_poi(df_destination)
    
        # Affichage du tableau de résultats    
        if poi_destination.empty:
            st.warning("Aucun point d'intérêt détecté pour cette destination.")
        else:
            st.title("Résultats de l'analyse des points d'intérêt :")
            st.table(poi_destination)
            # On sauvegarde les datasets en local
            poi_destination.to_csv(f"datas/poi_{search_query.replace(' ', '_').lower()}.csv", index=False)
            df_destination.to_csv(f"datas/dest_{search_query.replace(' ', '_').lower()}.csv", index=False)
    

