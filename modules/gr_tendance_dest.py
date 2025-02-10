import pandas as pd
import plotly.express as px

# Fonction pour générer un graphique interactif en ligne avec Plotly
def graph_dest_tendance(df_title):
    """
    Génère un graphique interactif avec Plotly et retourne `fig`.
    """
    if df_title.empty:
        return None  # Retourne `None` si pas de données

    # Conversion de l'année en entier
    df_title["Année"] = df_title["Année"].astype(int)

    # Comptage des vidéos par année
    video_counts = df_title["Année"].value_counts().sort_index()

    # Création du graphique interactif avec Plotly
    fig = px.line(
        x=video_counts.index, 
        y=video_counts.values, 
        markers=True,
        labels={"x": "Année", "y": "Nombre de vidéos"},
        title="Évolution du nombre de vidéos YouTube par année"
    )

    return fig  # Retourne `fig` pour l'affichage dans `app.py`
