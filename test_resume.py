from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
#from dotenv import load_dotenv
#load_dotenv()  # Charge les variables d'environnement depuis .env
import os
from pprint import pprint
GROQ_API_KEY = "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"

from langchain_groq import ChatGroq


# def summarize_transcript(input) -> str:

texte = """
[Music] what's up travelers ah beach to it what's up travelers it's liz and derek from means to travel and today we are back in the portsmouth area back at our airbnb and we decided just to do some quick little trips around portsmouth and kind of nearby areas we're going to start at portchester castle which is another english heritage site for us today and then we're gonna go to the town of winchester which has a ton of history so we'll talk to you when we get there but first we're gonna go check out this place okay so we started trying to figure out how to get into the castle and man we would have been terrible medieval invaders because we cannot even find a front entrance so um i just crossed like this river here it's not really a moat because i think it's natural um unless you think it's smoke oh yeah maybe because it does kind of go like around this castle here um again not a good invader don't even know my moats from my rivers um so i think we're going to go walk around the path in the opposite direction and wish us luck [Music] okay after walking around the entire castle we finally found the entrance [Music] okay also um their cafe has tapas which i was really impressed by okay so here we go walking [Music] in [Music] so we walked around literally the entire like outer walls [Music] we uh we can assure queen elizabeth that nobody is trying to invade other than us amass a huge today here ships were built and repaired and supplies of all kinds brought here and stockpiled one knight in 10 throughout the country was ordered to attend an armada was formed and on the 1st of may 1205 john took up residence here in the castle the preparations were made the soldiers were ready and willing but unfortunately the barons were not many of them had land in france as well as england and that made things a bit complicated for them all right we are entering the keep here at porchester it's so castle really cool we just listened to the audio guide on our phones which has tons of history portchester castle holds a commanding position at the head of a natural harbor making it the perfect location for anyone seeking to control the surrounding region the romans first constructed a castle here in the 3rd century aed as one of the line of coastal fortifications known as the forts of the saxon shore protecting roman britons from marauding saxon pirates the castle continued to be occupied throughout the saxon era all the way up to the norman conquest in 1066 at that point the existing norman structure began to take shape ultimately porchester became a royal castle under henry ii and remained property of the crown until 1632 in the intervening years it became a sometimes royal residence staging ground for repeated invasions of france and the site of a baronial mutiny after being sold by the crown porchester castle began to be used to house prisoners of war first housing dutch prisoners in 1655 and later prisoners in the napoleonic war from 1793 to 1815. during this time porchester housed up to 8 000 pows at any given time hey so we just toured through the keep here and now we're in um the inner bailey area as you can see there's nobody here with us there are a few people in um when we first got here in like the museum area in the keep but now we're just enjoying these old castle ruins and taking photos and we're about to go through the shop here before heading back out and hopefully heading over to winchester so it's been a really cool area lots of history plaques and what i was really delighted to see is there's like a whole room dedicated to the history of the caribbean or black prisoners that were sent here during the war between britain and france and like the late 1700s early 1800s so it was just really cool to learn just some black history while here too all right cheers [Music] hey so we just got in the car here at the castle we're about to head over to winchester but i wanted to just say a few things first so from a logistics standpoint we brought our own lunch um we actually brought this lunch box from the us so that we bought it actually in moab yeah and when we're doing like the national parks over there and we realized that on big road trips like we were doing then that it's great to be able to bring us packed lunch so we put everything in the like the little icy thing in the freezer and yes kept everything really cool so we have grapes and sandwich and a little bit of candy and i also put a roll of paper towels in here to act as napkins for us so just some little road trip tips for if you're driving around the uk or anywhere i also wanted to say that it was really cool to talk to the woman who is like working kind of the front entrance and shop because so we're here on a wednesday and it's a really nice day outside so really great day to go to the english heritage sites but there was nobody here and so we were talking to her a little bit about that and she was saying like this is one of the best years to go to these types of sites because a lot of it is outdoor still and they have hand sanitizer everywhere and um have like the social distancing requirements and on days like this especially on the weekdays there's nobody around um and she was even saying that she's like dipped to stonehenge she's like nobody's there she's like normally in the summer times they have 11 000 visitors a day and this year it's significantly less so she's like definitely get there while you guys are here in the uk so we will have to do that at some point but yeah we're about to eat our sandwiches now and just wanted to give those little tips and words of advice so this is a two-lane road um and it's beautiful we're in south house park oh no oh my god see folks that's how it's done this is so scary do the wave oh my god stop there [Music] the car is like you're going way too fast all right i am a scaredy cat but this is derek's third day driving in the uk [Music] so [Music] the hidden forest and we are on our way to winchester oh my gosh this is beautiful yeah it's telling you in that sign that it's gonna curve at the roundabout take the first exit this place has a roundabout [Music] police station it's a cute sign twenty a plenty [Music] [Music] so okay so i'm having like major anxiety riding in the passenger seat next to all these hedge walls in southbound national park with derek driving and he's just laughing at me and making fun of me and i'm having visions of what the next two months are gonna be like i'm so scared right now we're riding behind a semi truck that's at least setting the pace in a way that makes me feel slightly better than before say your prayers this is the oldest house in winchester built in 1450. it's a restaurant art supplies always make me feel so happy [Music] hubs always make me feel happy [Music] [Music] it's really pretty here this guy alfred the great is one of the powerhouses of english history credited with stitching together what would eventually become the kingdom of england or the land of the angles it was his descendants that would make winchester the first capital city of anglo-saxon england and cement its place in the history books the area surrounding winchester has a much more ancient heritage however having been the site of three iron age hill forts and becoming an important cultural center for the british belgae tribe prior to the roman conquest of britain it continued to thrive under the roman occupation and by the time of the roman abandonment was one of the largest cities on the island though not the largest or even second largest city in hampshire today winchester continues to be an important urban center in the region acting as hampshire's county town today winchester exudes a relaxed atmosphere hosting one of the largest farmers markets in england on the second and last sunday of each month hey everyone so we made it to winchester and we're walking along kind of this main pedestrian area in the downtown and it's 5 36 right now p.m and everything's closed which is a huge bummer i know that like a lot of smaller towns in the uk you kind of have to shut early and things might close at like five or six but like everything is already closed here except for the restaurant so i think we missed out on a little bit of fun just browsing and stuff but we get to do a little window shopping and then head back to portsmouth so hope you guys really like this montage of our walk through winchester this popular bronze statue imaginably titled horse and rider is one of three cast by world-renowned sculptor elizabeth frink in 1974. another the trio stands in london at the entrance to the royal academy of arts as the day drew to a close we made our way towards our last stop winchester cathedral although it was unfortunately closed by the time we arrived it is famous for being the final resting place of jane austen as well as the inspiration for the cathedral and ken fullet's pillars of the earth it's like your height and we're at our last stop of the day we're at winchester cathedral here in the town of winchester and um we're here right about dusk so it's just us and a few other maybe local college revelers hanging out around here but it's a really really pretty cathedral and has a lot of great kind of fall foliage trees if you walk around the ground and this town itself also has um a college so we've been walking around and seeing a lot of younger people here you can kind of hear them so it gives it a little bit more of a young feel from a lot of the other places that we've been touring around so it's a really cool place to just come visit and i really wish we had a little bit more time here in winchester but back to port so liz what are we doing we here searching for restrooms right here see a toilet use a toilet this is where you went i got sidetracked by a river typical story all right it is time for me to drive home for the first time in the rain in england hey travelers don't forget to subscribe and let's hang out more here are some links to other helpful travel videos on my channel and press that notification bell so you don't miss any new and awesome travel videos to come you
     """
if input is None :  # Vérifie si transcript est None ou vide
#if not input or input.isspace():
    print("Transcript vide ou non disponible.")  # Message par défaut si le transcript est invalide
try:
    #summary = summary_chain.run(transcript)
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.4,
        max_tokens=380,
        timeout=None,
        max_retries=2,
       
        api_key=GROQ_API_KEY
        # other params...       
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that summarize transcript from youtube.do your response must respond in french",
            ),
            ("human", "{input}"),
        ]
    )


    
    chain = prompt | llm
 
    result = chain.invoke({"input":texte})
    print(result.content)
except Exception as e:
    print(f"Erreur lors de la génération du résumé : {str(e)}")