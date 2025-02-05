from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
# ou bien  ? from langchain.prompts import ChatPromptTemplate
#from dotenv import load_dotenv
#load_dotenv()  # Charge les variables d'environnement depuis .env
import os
from pprint import pprint
GROQ_API_KEY = "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"

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
            "Extrait 10 points d'intérêt (POI) à partir du texte suivant. Liste-les sous forme de points :",
        ),
        ("human", "{texte_regroupe}"),
    ]
)

chain = prompt | llm
# ou bien chain = LLMChain(prompt=prompt, llm=llm) ?


# Fonction de résumé d'un transcript YouTube
def trouver_poi(texte_groupe) -> str:
    """Extraction poi avec LangChain."""
    if texte_groupe is None:  # Vérifie si transcript est None ou vide
        return "Transcript vide ou non disponible."  # Message par défaut si le transcript est invalide
    try:
        result = chain.invoke({"texte_regroupe": texte_groupe})
        return result.content
        # ou bien return result['text'] if 'text' in result else "Aucun texte généré."

    except Exception as e:
        return f"Erreur lors de la génération du résumé : {str(e)}"

# Exemple d'appel
#transcript_text = """
#YouTube est une plateforme de partage de vidéos utilisée par des millions de créateurs de contenu.
#Elle permet de publier, visionner, commenter et partager des vidéos sur une grande variété de sujets.
#"""
#summary = summarize_transcript(transcript_text)
#print("Résumé :", summary)

