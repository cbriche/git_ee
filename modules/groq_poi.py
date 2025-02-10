from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()  # Charge les variables d'environnement depuis .env
from pprint import pprint

# Récupération de la clé API Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY") # .env

from langchain_groq import ChatGroq

# Initialisation de llm et prompt en dehors de la fonction pour éviter de les recréer à chaque appel
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    model_kwargs={"max_completion_tokens":380},
    api_key=GROQ_API_KEY
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Tu es un expert  voyages.\n"
                "Donne-moi une liste de 10 points d'intérêt \n"
                "incontournables pour la destination suivante et  \n"
                "uniquement cette destination"
        ),
        ("human", "{search_query}"),
    ]
)

chain = prompt | llm


# Fonction de résumé d'un transcript YouTube
def trouver_poi(search_query) -> str:
    """Extraction poi avec LangChain."""
    if search_query is None:  # Vérifie si transcript est None ou vide
        return "Transcript vide ou non disponible."  # Message par défaut si le transcript est invalide
    try:
        result = chain.invoke({"search_query": search_query})
        return result.content
        # ou bien return result['text'] if 'text' in result else "Aucun texte généré."

    except Exception as e:
        return f"Erreur lors de la génération du résumé : {str(e)}"

# Ce bloc de code permet d'éviter que le script soit exécuté automatiquement lorsqu'il est 
# importé dans un autre fichier.
# Il ne s'exécute que si ce fichier est exécuté directement via `python liste_video_yt.py`.
if __name__ == "__main__":
    print("🔹 Test en mode standalone : ce script est exécuté directement.")

