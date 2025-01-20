import spacy
import pandas as pd
import multiprocessing
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Charger spaCy en mode rapide
try:
    nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger"])
except OSError:
    print("Le modèle spaCy n'est pas installé. Installation en cours...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger"])

# Instancier le modèle d’analyse des sentiments VADER
analyzer = SentimentIntensityAnalyzer()

def process_text(text):
    """ Fonction exécutée en parallèle pour extraire les POI et analyser le sentiment """
    if not text:
        return []

    doc = nlp(text)
    pois = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC", "FAC"]]
    if not pois:
        return []

    sentiment_score = analyzer.polarity_scores(text)["compound"]

    return [{"POI": poi, "Sentiment": sentiment_score} for poi in pois]

def top_10_poi(dataframe):
    """ Optimisation de l'extraction des POI et de l'analyse des sentiments avec multiprocessing """
    
    texts = dataframe["Transcript"].dropna().tolist()
    
    # Nombre optimal de processus
    num_workers = max(1, multiprocessing.cpu_count() - 1)

    # Multiprocessing Pool pour exécuter `process_text` en parallèle
    with multiprocessing.Pool(processes=num_workers) as pool:
        results = pool.map(process_text, texts)

    # Fusionner tous les résultats
    Liste_Poi_Sentiment = [item for sublist in results for item in sublist]

    if not Liste_Poi_Sentiment:
        return pd.DataFrame(columns=["POI", "Frequency", "AvgSentiment", "Score"])

    poi_destination = pd.DataFrame(Liste_Poi_Sentiment)

    # ⚡ OPTIMISATION : Groupby et aggregation en une seule passe
    poi_destination = poi_destination.groupby("POI").agg(
        Frequency=("POI", "count"),
        AvgSentiment=("Sentiment", "mean")
    ).reset_index()

    poi_destination["Score"] = poi_destination["Frequency"] * poi_destination["AvgSentiment"]**2
    poi_destination = poi_destination.sort_values(by="Score", ascending=False).head(10)

    return poi_destination
