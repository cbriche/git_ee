from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
#from dotenv import load_dotenv
#load_dotenv()  # Charge les variables d'environnement depuis .env
import os
from pprint import pprint
GROQ_API_KEY = "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"

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    max_completion_tokens = 380,
    api_key=GROQ_API_KEY
    # other params...
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that summarize transcript from youtube.",
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | llm
chain.invoke(
    {
        "input": "{input}",
    }
)

# Définition du prompt pour le résumé
#summary_prompt = PromptTemplate(
#    input_variables=["text"],
#    template="Fais un résumé concis du transcript suivant : {text}"
#)

# Création de la chaîne LangChain
#summary_chain = LLMChain(llm=llm, prompt=prompt)


# Fonction de résumé d'un transcript YouTube
def summarize_transcript(input) -> str:
    """Résumé d'un transcript YouTube avec LangChain."""
    if input is None :  # Vérifie si transcript est None ou vide
    #if not input or input.isspace():
        return "Transcript vide ou non disponible."  # Message par défaut si le transcript est invalide
    try:
        #summary = summary_chain.run(transcript)
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.4,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            max_completion_tokens = 380,
            api_key=GROQ_API_KEY
            # other params...       
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant that summarize transcript from youtube.",
                ),
                ("human", "bonjour et bienvenue au mali beau pays d'afrique de l'ouest"),
            ]
        )

        chain = prompt | llm
        result = chain.invoke(
            {
                "input": "bonjour et bienvenue au mali beau pays d'afrique de l'ouest",
            }
        )
        #return summary.strip()
        return result
    except Exception as e:
        return f"Erreur lors de la génération du résumé : {str(e)}"

# Exemple d'appel
#transcript_text = """
#YouTube est une plateforme de partage de vidéos utilisée par des millions de créateurs de contenu.
#Elle permet de publier, visionner, commenter et partager des vidéos sur une grande variété de sujets.
#"""
#summary = summarize_transcript(transcript_text)
#print("Résumé :", summary)

