# import des librairies
import streamlit as st
import pandas as pd
import os
import csv

#importe des fonctions depuis des modules externes
from modules.yt_qualif_dest import qualif_destination # Import de la fonction depuis le module externe
from modules.fonction_resumes import summarize_transcript # Import de la fonction depuis le module externe
from modules.fonction_poi import trouver_poi # Import de la fonction depuis le module externe

if "RUN_COUNT" not in st.session_state:
    st.session_state["RUN_COUNT"] = 0

st.session_state["RUN_COUNT"] += 1
print(f"🚀 Streamlit a exécuté ce script {st.session_state['RUN_COUNT']} fois.")


#on verifie une fois que le dossier datas existe sinon on le crée
os.makedirs("datas", exist_ok=True)

# titre de la page
st.title("Recherche de vidéos YouTube")

# Liste des mots-clés additionnels
mc_add = ['travel','tourism']   
# saisie de la destination par l'utisateur et elimination des espaces
search_query = st.text_input("Saisir ta destination (ville, pays, région, etc.)").strip()
clic_bouton = st.button(f'Obtenir les infos')  # Bouton pour lancer la recherche

# on ajoute les mots clés additionnels à la recherche
# Vérifie si l'utilisateur a saisi une destination (non vide après strip())
if search_query:  
    # Création d'une liste contenant chaque mot-clé associé à la destination
    search_keywords = " ".join([f"{search_query} {mc}" for mc in mc_add])

    # Construit la requête finale en ajoutant la destination seule + mots-clés associés
    full_query = f"{search_query} {search_keywords}"
else:
    # Si l'utilisateur n'a rien saisi, la requête est vide
    full_query = ""


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
        df_destination, video_ids = qualif_destination(full_query, search_query)
        print("Données récupérées - df_destination:", df_destination.shape, "- video_ids:", len(video_ids))
        
        if not video_ids:  # Vérifie si la liste est vide
            st.write("Aucune vidéo trouvée pour cette destination.")
            #st.stop()
            print("DEBUG: Colonnes actuelles de df_destination :", df_destination.columns)
    
        print('on appelle la fonction pour résumer les transcripts')
        df_destination['Résumés'] = df_destination['Transcript'].apply(summarize_transcript)
    
        #on affiche les résultats
        # st.title("Résumes des vidéos")
        # st.table(df_destination[['Title', 'Description','Transcript', 'Résumés']])
            
        # desc_regroupe = ' '.join(df_destination['Description'])
        # st.write(desc_regroupe)
            
        # On fusionne tous les résumés en un seul texte
        texte_regroupe = ' '.join(df_destination['Résumés'])
        # st.title("Texte regroupé des résumés")
        # st.write(texte_regroupe)
            
        print('On appelle la fonction pour trouver poi llm')
        mes_poi = trouver_poi(texte_regroupe)
        # Affichage du tableau de résultats
        st.title("Points d'intérêt détectés")
        st.write(mes_poi)
        
        
              
        
        # Enregistrement des POI dans un fichier CSV
        poi_csv_filename = f"datas/poi_{search_query.replace(' ', '_').lower()}.csv"
        
        with open(poi_csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Point d'Intérêt"])  # En-tête
            writer.writerow([mes_poi])  #Met tout le texte en une seule cellule

        print(f"Le fichier '{poi_csv_filename}' a été créé avec succès.")
    
        
        
        
        print(mes_poi)
        print(type(mes_poi))
            
        
            
        # if poi_destination.empty:
        #     st.warning("Aucun point d'intérêt détecté pour cette destination.")
        # else:
        #     st.title("Résultats de l'analyse des points d'intérêt :")
        #     st.table(poi_destination)
        #    
        # On sauvegarde les datasets en local
        # poi_destination.to_csv(f"datas/poi_{search_query.replace(' ', '_').lower()}.csv", index=False)
        df_destination.to_csv(f"datas/dest_{search_query.replace(' ', '_').lower()}.csv", index=False)
            
            