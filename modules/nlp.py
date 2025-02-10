# imortation des librairies
import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st

# Initialisation de l'analyseur
analyzer_vader = SentimentIntensityAnalyzer()

# création d'un new dataframe pour analyser les sentiments
# on part de df_destination

# Création du DF de travail
def crea_df_ana_sent(df_destination):
    """
    Création du DF de travail pour l'analyse de sentiments
    """
    df_ana_sent = df_destination[['Published At', 'Transcript', 'View Count', 'Comment Count']].copy()
    df_ana_sent['Année'] = pd.to_datetime(df_ana_sent['Published At']).dt.year
    df_ana_sent = df_ana_sent[['Année', 'Transcript', 'View Count', 'Comment Count']]
    return df_ana_sent


def clean_text(text):
    """ Nettoie le texte : supprime HTML, balises inutiles et caractères spéciaux """
    if not isinstance(text, str):  # Vérifie que le texte est bien une string
        return ""

    text = re.sub(r'\[.*?\]', '', text)  # Supprime les balises [Music], [Applause], etc.
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Supprime les URLs
    text = re.sub(r'<.*?>+', '', text)  # Supprime le HTML
    text = re.sub(r'[^A-Za-z0-9\s.,!?]', '', text)  # Garde seulement lettres, chiffres et ponctuation
    text = text.lower().strip()  # Minuscule + trim espaces

    return text


def analyze_sentiment(transcript):
    """ 
    Analyse le sentiment d'un transcript avec un ajustement équilibré :
    - Garde une bonne dispersion des scores.
    - Évite que tout soit bloqué autour de 0.70-0.79.
    - Réintroduit des scores élevés sans recréer l'effet "tout à 0.90".
    """
    if not transcript or pd.isna(transcript):
        return 0  # Neutralité si texte vide
    
    score = analyzer_vader.polarity_scores(transcript)["compound"]

    #  Ajustement final : meilleure diversité des scores positifs
    if score > 0:
        score = ((score ** 0.85) * 0.85) + (np.random.uniform(-0.1, 0.1))  # Ajout de variété
    elif score < 0:
        score = -((-score) ** 1.2)  # Amplification modérée des négatifs
    
    #  Limite les scores entre -1 et 1 pour rester logique
    score = max(-1, min(score, 1))

    return round(score, 3)  # Arrondi pour lisibilité




# 🔄 Dictionnaire de traduction des mots émotionnels
emotion_translation = {
    "amazing": "incroyable",
    "incredible": "incroyable",
    "unforgettable": "inoubliable",
    "magical": "magique",
    "wonderful": "merveilleux",
    "perfect": "parfait",
    "exceptional": "exceptionnel",
    "fantastic": "fantastique",
    "awesome": "génial",
    "expensive": "cher",
    "crowded": "bondé",
    "boring": "ennuyeux",
    "disappointing": "décevant",
    "scam": "arnaque",
    "terrible": "terrible",
    "awful": "horrible",
    "bad": "mauvais",
    "annoying": "agaçant"
}

# 🔥 1️⃣ Détection des mots émotionnels (ANGLAIS → FRANÇAIS)
def extract_emotional_words(transcripts):
    """ Détecte les mots émotionnels les plus fréquents et les traduit en français """
    english_words = set(emotion_translation.keys())
    word_counts = Counter()

    for text in transcripts.dropna():
        words = text.lower().split()
        for word in words:
            if word in english_words:
                word_counts[word] += 1

    # Traduire les mots détectés
    translated_counts = {emotion_translation[word]: count for word, count in word_counts.most_common(10)}
    
    return translated_counts



def plot_wordcloud(emotion_words):
    """ Génère un nuage de mots basé sur les mots émotionnels extraits """
    if not emotion_words:
        st.write("Aucun mot émotionnel détecté.")
        return

    # Convertir les mots émotionnels en une string pour WordCloud
    word_freq = {word: freq for word, freq in emotion_words.items()}
    
    wordcloud = WordCloud(
        width=800, height=400, background_color="white", colormap="coolwarm"
    ).generate_from_frequencies(word_freq)

    # Affichage du nuage de mots
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")  # Pas d'axes pour le word cloud
    st.pyplot(fig)




# # Extraction des thèmes principaux avec TF-IDF
# def extract_top_themes(transcripts, num_keywords=5):
#     """ 
#     Utilise TF-IDF pour extraire les thèmes dominants avec stopwords et optimisation.
#     - Supprime les mots inutiles ("just", "like", "going").
#     - Garde uniquement les noms les plus fréquents.
#     - Ajoute une analyse en bigrammes (ex: "mauvais service", "prix élevé").
#     """
#     custom_stopwords = set([
#         "just", "like", "going", "youre", "get", "really", "one", "thing", "know", 
#         "people", "want", "even", "make", "dont", "way", "ive", "can", "now"
#     ])

#     vectorizer = TfidfVectorizer(
#         stop_words="english", 
#         max_features=25,  # On réduit le nombre de mots pour accélérer
#         ngram_range=(1,2)  # Analyse aussi les bigrammes (expressions de 2 mots)
#     )

#     tfidf_matrix = vectorizer.fit_transform(transcripts.dropna())
#     feature_names = vectorizer.get_feature_names_out()
#     scores = tfidf_matrix.sum(axis=0).A1
#     keywords = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)

#     # 🔍 On filtre pour garder que les termes utiles
#     filtered_keywords = [word for word, _ in keywords if word not in custom_stopwords]

#     return filtered_keywords[:num_keywords]

  










