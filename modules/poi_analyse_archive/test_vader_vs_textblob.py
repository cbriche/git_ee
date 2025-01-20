import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# Instancier les analyseurs
analyzer_vader = SentimentIntensityAnalyzer()

def analyze_with_vader(text):
    return analyzer_vader.polarity_scores(text)["compound"]

def analyze_with_textblob(text):
    return TextBlob(text).sentiment.polarity

# 🔹 Simule un transcript YouTube long (extrait réel recommandé)
transcript = """
What's up guys, we're here in Cancun 
and in this video we're going to show   you the best things to do in and around the area.   So there's beautiful cenotes, ancient ruins, 
and of course some really beautiful beaches too,   and we found a secret spot which we can't 
wait to show you. So enjoy this video! We are Zac and Ine. Full-time digital 
nomads from the United States and Belgium.   We met while studying abroad in 2018 and have 
been traveling the world together ever since.   We're here to inspire your next adventure, 
whether it's hiking in the Canadian Rockies,   a road trip through the US, or backpacking 
across Africa. On our channel, you'll find   unfiltered videos of hiking guides and the best 
things to do in destinations around the world. Located in the northeast of the Yucatan 
Peninsula, Cancun borders the Caribbean Sea.   It's known for its white sand beaches, 
turquoise sea, numerous resorts, and   nightlife. The city is composed of two distinct 
areas: the more local downtown area, El Centro,   and Zona Hotelera, a long beachfront strip 
of high-rise hotels, nightclubs, shops,   and restaurants. Cancun is known around the world 
as the party capital of Mexico, with great air and   ground transportation connectivity. But there's 
so many more things to do in Cancun besides just   the nightlife. In this video, we'll show you 
the top 10 things to do in and around Cancun. The Cancun Scenic Tower is the highest attraction 
in the Riviera Maya. Here, you can take a ride up   to an altitude of 262 feet or 80 meters. 
You can take photos while the deck spins   giving you 360 degree views of the entire Hotel 
Zone. You can also learn a bit about the history   of Cancun through the audio commentary. The total 
viewpoint experience lasts about 15 to 20 minutes. The ninth best thing to do in Cancun is to visit 
the downtown area. Downtown Cancun offers a great   taste of local culture, with delicious 
street food, small shops, and cute parks.   This is the area where the locals live 
and this is visible in the prices as well.   You'll find more affordable souvenir shops and 
eateries here than in the Hotel Zone, with prices   being sometimes three times cheaper. Wander down 
Avenida Tulum and experience the real Cancun. At number eight we have a truly 
refreshing and unique experience:   swimming in the nearby cenotes. 
The Yucatan Peninsula in general   is well known for its cenotes, with as many as 
six thousand of them scattered around the area.   Our favorite cenotes near Cancun include the 
Cenote Azul, Gran Cenote, Sac Actun, and Calavera   Cenote. But, if you're looking for ones that are 
closer, head to the Ruta de los Cenotes. It's best   to rent a car for the day if you want to visit a 
few of them as most cenotes are in the middle of   nowhere. However, many day tours also combine 
at least one cenote with other attractions. Yeah it's very cool like 
we're in a little cave here,   but you can also do a lot of really 
cool jumps from like the rocks above us. The Hotel Zone is the primary tourist 
area filled with high-rise hotels,   shops, bars, and many restaurants. It's a 15 
mile wide or 24 kilometer strip of beautiful   white-sand beaches and deep blue water and 
thus it's where most people decide to stay.   However, it can also get 
very crowded and expensive.   There's only one road, the Kukulcan Boulevard, 
which runs from one side to the other. Playa Chac   Mool is gorgeous, but it's very wavy. It's also 
a great place to print water sports equipment. As briefly explained at the start of this 
video, Cancun is the party capital of Mexico   and so we can't talk about the city 
without mentioning the nightlife.   Most nightclubs are located in the 
Hotel Zone and can get pretty wild.   Coco Bongo is the most popular club in Cancun, 
featuring acrobats, cover bands, and DJs.   But, there are many other clubs such as Señor 
Frogs, Mandala Beach Club, and the City Nightclub.   All of them offer something different 
but can have long wait lines. Located along a more quiet part of the Hotel Zone, 
Playa Tortugas is our favorite beach in the zone.   It has public access and offers a more local 
experience with a relaxed atmosphere and clean   sands. It's also better for swimming as the water 
is calm and there's generally less wind here.   Therefore, it's ideal for families with kids.   This beach also boasts several open-air 
restaurants with seafood dishes and drinks. So besides relaxing or renting a jet 
ski at Playa Tortugas, you can also   bungee jump if you're looking for some adrenaline. 
So there's a guy about to jump right now. The fourth best thing to do in Cancun is to 
go on a day trip to the nearby Isla Mujeres.   Only a 20 minute boat ride from Cancun, Isla 
Mujeres is a peaceful paradise known for its   white-sand beaches, crystal clear waters, and the 
friendliest locals in the Mexican Caribbean. The   island is small so you can get around it easily 
by golf cart or bike. Make sure to watch the   sea turtles at the local turtle farm, visit the 
Mayan ruins and cliffs at Punta Sur, and watch the   sunset at Playa Norte. Find more details about a 
day tour to Isla Mujeres in the description below. About 12 and a half miles or 20 kilometers north 
of the city of Cancun sits the stunning Isla   Blanca. You can get here by local colectivo, which 
leaves near the "Farmacia Canto" at the corner   of Avenida Lopez Portillo and Calle 7, about 
three times a day. We got off at the last stop   which is the thinnest part of the peninsula. 
This untouched peninsula is a true hidden gem,   with the turquoise Caribbean sea on one side and 
an immense laguna with kiteboarders on the other.   You feel a thousand miles away from 
the hustle and bustle of Cancun. So we're walking the beaches of Isla Blanca 
here and it's so peaceful compared to the   rest of Cancun. It's really a hidden 
gem. One thing you should do though   is make sure you bring your own food and 
drinks, because there's literally nothing   out here. And you're kind of on your own. 
But it's really peaceful, you should come A trip to Cancun isn't complete without 
visiting one of the 7 World Wonders.   Chichén Itzá is located about three hours away 
from Cancun by car or tour bus. It was once a   vibrant city with a diverse population of Mayan 
people extending well into the tens of thousands.   Today, it's one of the most visited 
archaeological sites in all of Mexico.   The "El Castillo Pyramid" in the site center 
is the most iconic and spectacular Mayan   ruin of the entire archaeological site. 
Find a link in the description below to   book your own Chichén Itzá day tour, which 
combines the ruins with a beautiful cenote. The best thing to do in Cancun in our opinion 
is to go scuba diving or snorkeling at the MUSA   Underwater Museum of Art as well as the Manchones 
Reef. Located only 30 minutes away from Cancun,   this underwater museum is home to 500 life-size 
sculptures that are used to promote coral, algae,   and other marine life. It's arguably the largest 
museum of its kind anywhere on earth. But besides   this museum, there's also a beautiful reef nearby. 
The Manchones Reef is home to various types of   fish, sea turtles, and rays. Find more info about 
a dive and snorkel tour in the description below. All right guys, that's it for our video on the 
best things to do in Cancun. We really hope you   enjoyed it. Make sure to check out our other video 
where we highlight five must-do day trips from   Cancun. Like this video if you found it helpful, 
subscribe to our channel for more Mexico videos,   and download our free giveaway in the description 
below. Catch you on the next adventure!
"""

# 🔹 Compter le nombre de mots
word_count = len(transcript.split())

# 🔹 Test de vitesse et analyse avec VADER
start = time.time()
vader_score = analyze_with_vader(transcript)
vader_time = time.time() - start

# 🔹 Test de vitesse et analyse avec TextBlob
start = time.time()
textblob_score = analyze_with_textblob(transcript)
textblob_time = time.time() - start

# 🔹 Affichage des résultats
print(f"Nombre de mots : {word_count}")
print(f"VADER Score : {vader_score} | Temps : {vader_time:.4f} sec")
print(f"TextBlob Score : {textblob_score} | Temps : {textblob_time:.4f} sec")
