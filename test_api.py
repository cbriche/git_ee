
GROQ_API_KEY = "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"
from langchain_groq import ChatGroq



llm = ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)

# Liste des modèles disponibles
available_models = [
    "llama-3.1-8b-instant",
    "llama-2-7b-chat",
    "mistral-7b",
    "mixtral-8x7b"
]

print("🔍 Test des modèles disponibles sur Groq :")
for model in available_models:
    try:
        llm = ChatGroq(model=model, api_key=GROQ_API_KEY)
        print(f"✅ Modèle disponible : {model}")
    except Exception as e:
        print(f"❌ Modèle indisponible : {model} ({e})")

available_models = ["llama-3.1-8b-instant", "llama-2-7b-chat", "mistral-7b", "mixtral-8x7b"]

for model in available_models:
    print(f"🔍 Test du modèle : {model}")
    try:
        llm = ChatGroq(model=model, api_key=GROQ_API_KEY)
        response = llm.invoke("Donne-moi un résumé de la Tour Eiffel en trois phrases.")
        print(f"✅ Réponse de {model} : {response.content[:100]}...")  # Affiche un aperçu
    except Exception as e:
        print(f"❌ Échec avec {model} : {e}")