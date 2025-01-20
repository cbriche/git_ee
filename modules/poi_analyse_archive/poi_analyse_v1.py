import spacy
from textblob import TextBlob
import pandas as pd

try:
    nlp = spacy.load("en_core_web_sm")  # Vérifie si le modèle est installé
except OSError:
    print("Le modèle en_core_web_sm n'est pas installé. Installation en cours...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    # Charger le modèle spaCy pour identifier les entités nommées (villes, pays, monuments...)
    # Extraction d'entités nommées NER (Named Entity Recognition) lieux, personnes organisation, date etc...
    nlp = spacy.load("en_core_web_sm")  # Charger après installation


def top_10_poi(dataframe):
    #creation d'une liste vide pour stocker les POI
    Liste_Poi_Sentiment = []
    #normalement, je n'ai pas lire le csv, c'est df_destination qui est en paramètre
    for index, row in dataframe.iterrows():
        #on récupère le transcript
        text = str(row.get("Transcript", "")).strip()
        if not text:
            continue
        # on extrait les lieux du transcript par vidéo
        doc = nlp(text)
        # Extraire les entités d'intérêt (lieux, monuments, infrastructures)
        # GPE c'est les lieux = ville, pays, région, 
        # LOC c'est les monuments = musée, château, église, etc...,
        # FAC c'est les infrastructures = aéroport, gare, etc...
        # on crée une liste de comprehension pour récupérer les lieux
        pois = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC", "FAC"]]
        # si une liste pois ne contient aucun Poi, on met None
        if not pois:
            pois = ["Aucun POI détecté"]
        
        #on récupère les sentiments et la note pour chaque POI
        #on utilise textblob pour analyser le sentiment
        #pouquoi textblob ? car il est plus simple et plus rapide que spacy
        blob = TextBlob(text)
        # il permet la découpe de texte en phrases via sentences
        # pour chaque phrase, on récupère le sentiment
        for sentence in blob.sentences:
            #pour chaque phrase, on regarde si le POI est présent
            for poi in pois:  
                #si le POI est présent dans la phrase alosr on récupère le sentiment
                if poi in sentence:
                    sentiment_score = sentence.sentiment.polarity  
                    # Ajouter POI et sentiment à la liste
                    Liste_Poi_Sentiment.append({"POI": poi, "Sentiment": sentiment_score})
    
    #je crée un dataframe avec les POI et le sentiment
    poi_destination = pd.DataFrame(Liste_Poi_Sentiment)
    
    #on groupe par POI  
    poi_destination = poi_destination.groupby("POI").agg(
    #on fait la somme de chaque POI
    Frequency=("POI", "count"),
    #on fait la moyenne des sentiments par POI
    AvgSentiment=("Sentiment", "mean")
    ).reset_index()
    
    # Classement final
    #Prendre la valeur absolue du sentiment pour éviter les biais
    poi_destination["Score"] = poi_destination["Frequency"] * poi_destination["AvgSentiment"]**2
    poi_destination = poi_destination.sort_values(by="Score", ascending=False).head(10)
    
    return poi_destination
    
    
    
        
    









# Ce bloc de code permet d'éviter que le script soit exécuté automatiquement lorsqu'il est 
# importé dans un autre fichier.
# Il ne s'exécute que si ce fichier est exécuté directement via `python recup_url_yt.py`.
if __name__ == "__main__":
    print("🔹 Test en mode standalone : ce script est exécuté directement.")