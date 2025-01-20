import spacy
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Charger spaCy en mode rapide (désactiver ce qui n’est pas utile)
try:
    nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger"])
except OSError:
    print("Le modèle spaCy n'est pas installé. Installation en cours...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger"])

# Instancier le modèle d’analyse des sentiments VADER
analyzer = SentimentIntensityAnalyzer()

def top_10_poi(dataframe):
    """Optimisation de l'extraction des POI et de l'analyse des sentiments"""
    
    Liste_Poi_Sentiment = []
    
    # ⚡ OPTIMISATION : Utilisation de nlp.pipe() pour traiter tous les textes en une seule passe
    texts = dataframe["Transcript"].dropna().tolist()
    docs = list(nlp.pipe(texts))  # Traitement en batch

    # Associer chaque doc traité à la ligne du DataFrame
    for index, (row, doc) in enumerate(zip(dataframe.itertuples(), docs)):
        pois = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC", "FAC"]]
        if not pois:
            continue  # Skip si aucun POI détecté

        # ⚡ OPTIMISATION : Utilisation de VADER pour une analyse rapide
        sentiment_score = analyzer.polarity_scores(row.Transcript)["compound"]

        # Ajouter chaque POI détecté avec son sentiment
        for poi in pois:
            Liste_Poi_Sentiment.append({"POI": poi, "Sentiment": sentiment_score})

    # Transformer directement la liste en DataFrame sans boucle intermédiaire
    poi_destination = pd.DataFrame(Liste_Poi_Sentiment)

    if poi_destination.empty:
        return pd.DataFrame(columns=["POI", "Frequency", "AvgSentiment", "Score"])

    # Utilisation de `agg()` pour faire tous les calculs en une seule passe
    poi_destination = poi_destination.groupby("POI").agg(
        Frequency=("POI", "count"),
        AvgSentiment=("Sentiment", "mean")
    ).reset_index()

    # Calcul du score final
    poi_destination["Score"] = poi_destination["Frequency"] * poi_destination["AvgSentiment"]**2
    poi_destination = poi_destination.sort_values(by="Score", ascending=False).head(10)

    return poi_destination
