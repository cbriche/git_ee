# Projet : Explor'Emotion (démarrage)

## **Description du Projet**
Ce projet analyse des données YouTube pour explorer une destination à travers trois axes principaux :

1. **Guide des 10 POI les plus recommandés** : Identification des lieux les plus mentionnés et recommandés par les vidéos YouTube.
2. **Analyse des perceptions et émotions** : Extraction et analyse des sentiments exprimés par les créateurs de contenu.
3. **Identification des tendances émergentes** : Détection des lieux ou expériences gagnant en popularité.

---

## **Technologies Utilisées**
- **Python** : Analyse et traitement des données.
- **API YouTube Data v3** : Extraction des métadonnées des vidéos.
- **youtube-transcript-api** : Récupération des sous-titres.
- **Bibliothèques NLP** : spaCy, TextBlob pour l'analyse sémantique et des sentiments.

---

## **Installation**
1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/votre-projet.git
   cd votre-projet
   ```
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Ajoutez votre clé API dans un fichier `.env` :
   ```
   API_KEY=YOUR_API_KEY
   ```

---

## **Utilisation**
1. **Configurer les mots-clés et paramètres** dans le fichier principal.
2. Lancez le script principal :
   ```bash
   python main.py
   ```

---

## **Auteurs**
- **Nom 1** : Extraction des données.
- **Nom 2** : Analyse des émotions.
- **Nom 3** : Identification des tendances.