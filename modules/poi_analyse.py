# Description: Module pour l'analyse de sentiment hybride (VADER et TextBlob)
import spacy
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import concurrent.futures

#installer la vocab : python -m spacy download en_core_web_sm

# Charger spaCy en mode rapide (désactiver ce qui n’est pas utile)
try:
    nlp = spacy.load("en_core_web_sm", disable=["parser"])
except OSError:
    print("Le modèle spaCy n'est pas installé. Installation en cours...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm", disable=["parser"])

# Instancier les analyseurs
analyzer_vader = SentimentIntensityAnalyzer()

def analyze_sentiment(transcript):
    """ Utilise VADER pour les courts textes et TextBlob pour les longs textes """
    word_count = len(transcript.split())

    if word_count < 500:
        return analyzer_vader.polarity_scores(transcript)["compound"]  # VADER rapide
    else:
        return TextBlob(transcript).sentiment.polarity  # TextBlob pour plus de précision

def process_text(text):
    """ Fonction exécutée en parallèle pour extraire les POI et analyser le sentiment """
    if not text:
        return []

    doc = nlp(text)
    pois = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC", "FAC"]]
    if not pois:
        return []

    sentiment_score = analyze_sentiment(text)  # Utilisation de la stratégie hybride

    return [{"POI": poi, "Sentiment": sentiment_score} for poi in pois]

def top_10_poi(dataframe):
    """ Optimisation de l'extraction des POI et de l'analyse des sentiments avec multiprocessing """
    
    texts = dataframe["Transcript"].dropna().tolist()
    
    # Nombre optimal de threads (peut être ajusté)
    max_workers = min(10, len(texts))  # On évite trop de threads inutiles

     # Utilisation de ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(process_text, texts)

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
