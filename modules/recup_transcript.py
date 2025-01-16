#recupération des transcript

from youtube_transcript_api import YouTubeTranscriptApi

# récupération d'un transcript
transcription = YouTubeTranscriptApi.get_transcript('ndM4YzkqjMg', languages=['fr'])

#seul les textes m'intéressent, l'api retourne un dictionnaire
#je récupérer la valeur de la cle text

#utilisation d'une comprhésension de liste pour récupérer les textes plus rapide qu'une boucle for
transcript_text = " ".join([untext['text'] for untext in transcription])
   
  