"""Naruto: Shinobi Trials — a self-contained Streamlit quiz game.

Run with:
    streamlit run quiz_master.py
"""

import random
import re
import time

import streamlit as st


st.set_page_config(
    page_title="Naruto: Shinobi Trials",
    page_icon="🍥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# More than 20 questions are included; each game uses a fresh random set of 20.
QUESTION_BANK = [
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Mercury"],
        "answer": "Mars",
        "explanation": "Iron-rich minerals in Mars's soil give the planet its distinctive reddish appearance.",
        "category": "Space",
    },
    {
        "question": "What is the capital city of Japan?",
        "options": ["Kyoto", "Seoul", "Tokyo", "Osaka"],
        "answer": "Tokyo",
        "explanation": "Tokyo is Japan's capital and its largest metropolitan area.",
        "category": "Geography",
    },
    {
        "question": "Which element has the chemical symbol O?",
        "options": ["Gold", "Osmium", "Oxygen", "Oganesson"],
        "answer": "Oxygen",
        "explanation": "O is the standard chemical symbol for oxygen, atomic number 8.",
        "category": "Science",
    },
    {
        "question": "Who wrote the play Romeo and Juliet?",
        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Oscar Wilde"],
        "answer": "William Shakespeare",
        "explanation": "Romeo and Juliet is one of Shakespeare's best-known tragedies.",
        "category": "Literature",
    },
    {
        "question": "What is 9 × 8?",
        "options": ["63", "72", "81", "64"],
        "answer": "72",
        "explanation": "Nine multiplied by eight equals seventy-two.",
        "category": "Math",
    },
    {
        "question": "Which ocean is the largest on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "answer": "Pacific Ocean",
        "explanation": "The Pacific Ocean covers more area than all of Earth's land combined.",
        "category": "Geography",
    },
    {
        "question": "What do bees collect from flowers to make honey?",
        "options": ["Nectar", "Chlorophyll", "Pollen only", "Sap"],
        "answer": "Nectar",
        "explanation": "Bees collect nectar, then transform it into honey in the hive.",
        "category": "Nature",
    },
    {
        "question": "Which instrument typically has 88 keys?",
        "options": ["Violin", "Piano", "Flute", "Trumpet"],
        "answer": "Piano",
        "explanation": "A modern standard piano normally has 52 white keys and 36 black keys.",
        "category": "Arts",
    },
    {
        "question": "In which country are the Pyramids of Giza located?",
        "options": ["Greece", "Egypt", "Mexico", "Italy"],
        "answer": "Egypt",
        "explanation": "The Giza pyramid complex lies near Cairo, Egypt.",
        "category": "History",
    },
    {
        "question": "What is the freezing point of water at sea level in Celsius?",
        "options": ["0°C", "32°C", "10°C", "100°C"],
        "answer": "0°C",
        "explanation": "Pure water freezes at 0°C (32°F) at standard atmospheric pressure.",
        "category": "Science",
    },
    {
        "question": "Which language is primarily used to style web pages?",
        "options": ["HTML", "Python", "CSS", "SQL"],
        "answer": "CSS",
        "explanation": "CSS (Cascading Style Sheets) controls the visual presentation of web pages.",
        "category": "Technology",
    },
    {
        "question": "Which animal is the largest mammal?",
        "options": ["African elephant", "Blue whale", "Giraffe", "Hippopotamus"],
        "answer": "Blue whale",
        "explanation": "The blue whale is the largest animal known to have existed.",
        "category": "Nature",
    },
    {
        "question": "How many continents are commonly recognized?",
        "options": ["5", "6", "7", "8"],
        "answer": "7",
        "explanation": "The commonly taught model includes Africa, Antarctica, Asia, Europe, North America, South America, and Australia.",
        "category": "Geography",
    },
    {
        "question": "Which artist painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"],
        "answer": "Leonardo da Vinci",
        "explanation": "Leonardo da Vinci painted the Mona Lisa in the early 16th century.",
        "category": "Arts",
    },
    {
        "question": "What is the square root of 144?",
        "options": ["10", "11", "12", "14"],
        "answer": "12",
        "explanation": "12 × 12 equals 144.",
        "category": "Math",
    },
    {
        "question": "Which organ pumps blood around the human body?",
        "options": ["Lungs", "Brain", "Heart", "Liver"],
        "answer": "Heart",
        "explanation": "The heart is a muscular organ that pumps blood through the circulatory system.",
        "category": "Science",
    },
    {
        "question": "What is the first month of the year?",
        "options": ["December", "January", "February", "March"],
        "answer": "January",
        "explanation": "January begins the Gregorian calendar year.",
        "category": "Everyday",
    },
    {
        "question": "Which gas do plants absorb from the air during photosynthesis?",
        "options": ["Oxygen", "Nitrogen", "Carbon dioxide", "Helium"],
        "answer": "Carbon dioxide",
        "explanation": "Plants use carbon dioxide, water, and light energy to make sugars during photosynthesis.",
        "category": "Science",
    },
    {
        "question": "Who was the first person to walk on the Moon?",
        "options": ["Buzz Aldrin", "Yuri Gagarin", "Neil Armstrong", "John Glenn"],
        "answer": "Neil Armstrong",
        "explanation": "Neil Armstrong stepped onto the Moon during Apollo 11 in 1969.",
        "category": "History",
    },
    {
        "question": "Which shape has three sides?",
        "options": ["Square", "Pentagon", "Triangle", "Circle"],
        "answer": "Triangle",
        "explanation": "A triangle is a polygon with exactly three sides and three angles.",
        "category": "Math",
    },
    {
        "question": "What is the currency used in the United Kingdom?",
        "options": ["Euro", "Dollar", "Pound sterling", "Yen"],
        "answer": "Pound sterling",
        "explanation": "The United Kingdom uses pound sterling, commonly called the pound.",
        "category": "Geography",
    },
    {
        "question": "Which planet is famous for its prominent rings?",
        "options": ["Saturn", "Earth", "Neptune", "Mars"],
        "answer": "Saturn",
        "explanation": "Saturn's bright rings are mostly made of ice particles, dust, and rock.",
        "category": "Space",
    },
    {
        "question": "What is the main ingredient in traditional guacamole?",
        "options": ["Tomato", "Avocado", "Potato", "Cucumber"],
        "answer": "Avocado",
        "explanation": "Mashed avocado is the base of traditional guacamole.",
        "category": "Food",
    },
    {
        "question": "Which word is a synonym for 'rapid'?",
        "options": ["Slow", "Quick", "Quiet", "Heavy"],
        "answer": "Quick",
        "explanation": "Rapid and quick both describe something that moves or happens fast.",
        "category": "Language",
    },
    {
        "question": "How many days are there in a leap year?",
        "options": ["364", "365", "366", "367"],
        "answer": "366",
        "explanation": "A leap year adds February 29, bringing the total to 366 days.",
        "category": "Everyday",
    },
    {
        "question": "Which continent is the Sahara Desert on?",
        "options": ["Asia", "South America", "Africa", "Australia"],
        "answer": "Africa",
        "explanation": "The Sahara stretches across much of North Africa.",
        "category": "Geography",
    },
    {
        "question": "What is the largest internal organ in the human body?",
        "options": ["Heart", "Lung", "Liver", "Kidney"],
        "answer": "Liver",
        "explanation": "The liver is the body's largest internal organ and has many vital functions.",
        "category": "Science",
    },
    {
        "question": "Which programming language is named after a British comedy group?",
        "options": ["Java", "Python", "Ruby", "Swift"],
        "answer": "Python",
        "explanation": "Python's creator named it after Monty Python, not the snake.",
        "category": "Technology",
    },
    {
        "question": "What is the opposite of 'transparent'?",
        "options": ["Opaque", "Clear", "Bright", "Reflective"],
        "answer": "Opaque",
        "explanation": "An opaque material does not let light pass through it clearly.",
        "category": "Language",
    },
    {
        "question": "Which is the fastest land animal?",
        "options": ["Lion", "Cheetah", "Horse", "Greyhound"],
        "answer": "Cheetah",
        "explanation": "A cheetah can reach bursts of speed around 100–120 km/h (62–75 mph).",
        "category": "Nature",
    },
]


# Naruto and Naruto Shippuden question bank. A mission draws 20 random questions.
QUESTION_BANK = [
    {"question": "What is the title given to the leader of Konohagakure?", "options": ["Kazekage", "Hokage", "Mizukage", "Raikage"], "answer": "Hokage", "explanation": "The Hokage is the leader of the Hidden Leaf Village.", "category": "Hidden Leaf"},
    {"question": "Who is Naruto Uzumaki's father?", "options": ["Jiraiya", "Minato Namikaze", "Hiruzen Sarutobi", "Kakashi Hatake"], "answer": "Minato Namikaze", "explanation": "Minato Namikaze, the Fourth Hokage, is Naruto's father.", "category": "Characters"},
    {"question": "Who is Naruto Uzumaki's mother?", "options": ["Tsunade", "Mikoto Uchiha", "Kushina Uzumaki", "Konan"], "answer": "Kushina Uzumaki", "explanation": "Kushina Uzumaki was Naruto's mother and the previous Nine-Tails jinchuriki.", "category": "Characters"},
    {"question": "Which tailed beast is sealed inside Naruto?", "options": ["Shukaku", "Kurama", "Gyuki", "Son Goku"], "answer": "Kurama", "explanation": "Kurama is the Nine-Tailed Fox sealed within Naruto.", "category": "Tailed Beasts"},
    {"question": "Who are Naruto's teammates on Team 7?", "options": ["Sakura and Sasuke", "Neji and Rock Lee", "Shino and Kiba", "Choji and Shikamaru"], "answer": "Sakura and Sasuke", "explanation": "Team 7 begins with Naruto, Sakura Haruno, and Sasuke Uchiha under Kakashi.", "category": "Teams"},
    {"question": "Which dojutsu is inherited by the Uchiha clan?", "options": ["Byakugan", "Rinnegan", "Sharingan", "Tenseigan"], "answer": "Sharingan", "explanation": "The Sharingan is the Uchiha clan's signature visual jutsu.", "category": "Clans & Dojutsu"},
    {"question": "Who taught Naruto the Rasengan?", "options": ["Kakashi", "Jiraiya", "Iruka", "Yamato"], "answer": "Jiraiya", "explanation": "Jiraiya taught Naruto the Rasengan, a technique created by Minato.", "category": "Jutsu"},
    {"question": "Who created the Chidori?", "options": ["Sasuke Uchiha", "Kakashi Hatake", "Itachi Uchiha", "Orochimaru"], "answer": "Kakashi Hatake", "explanation": "Kakashi invented the Chidori and later taught it to Sasuke.", "category": "Jutsu"},
    {"question": "Which jutsu does Naruto learn from the Scroll of Seals?", "options": ["Flying Raijin", "Multi Shadow Clone Jutsu", "Chidori", "Summoning Jutsu"], "answer": "Multi Shadow Clone Jutsu", "explanation": "Naruto learns the Multi Shadow Clone Jutsu from the forbidden Scroll of Seals.", "category": "Jutsu"},
    {"question": "Who becomes the Fifth Hokage?", "options": ["Tsunade", "Kurenai", "Anko", "Temari"], "answer": "Tsunade", "explanation": "Tsunade returns to Konoha and becomes its Fifth Hokage.", "category": "Kage"},
    {"question": "Who was the Fourth Hokage of Konoha?", "options": ["Tobirama Senju", "Minato Namikaze", "Hiruzen Sarutobi", "Hashirama Senju"], "answer": "Minato Namikaze", "explanation": "Minato Namikaze was the Fourth Hokage, also called the Yellow Flash.", "category": "Kage"},
    {"question": "Which tailed beast was sealed inside Gaara?", "options": ["Kurama", "Shukaku", "Matatabi", "Saiken"], "answer": "Shukaku", "explanation": "Gaara was the jinchuriki of Shukaku, the One-Tailed beast.", "category": "Tailed Beasts"},
    {"question": "What is the name of Gaara's village?", "options": ["Hidden Mist", "Hidden Stone", "Hidden Sand", "Hidden Cloud"], "answer": "Hidden Sand", "explanation": "Gaara is a shinobi of Sunagakure, the Hidden Sand Village.", "category": "Villages"},
    {"question": "Who temporarily leads Team 7 during Kakashi's absence in Shippuden?", "options": ["Yamato", "Guy", "Asuma", "Iruka"], "answer": "Yamato", "explanation": "Yamato joins Team 7 and helps contain Naruto's Nine-Tails chakra.", "category": "Teams"},
    {"question": "What was the Akatsuki's main objective?", "options": ["Protect the Five Kage", "Collect the tailed beasts", "Restore the Uchiha clan", "Find the Sage of Six Paths"], "answer": "Collect the tailed beasts", "explanation": "Akatsuki captured the jinchuriki to gather all nine tailed beasts.", "category": "Akatsuki"},
    {"question": "What is Pain's true name?", "options": ["Yahiko", "Nagato", "Obito", "Kabuto"], "answer": "Nagato", "explanation": "Nagato uses the Six Paths of Pain to act as Akatsuki's apparent leader.", "category": "Akatsuki"},
    {"question": "Who defeats Asuma Sarutobi?", "options": ["Kakuzu", "Hidan", "Orochimaru", "Deidara"], "answer": "Hidan", "explanation": "Hidan kills Asuma with his ritual technique; Shikamaru later takes revenge.", "category": "Akatsuki"},
    {"question": "Which clan does Shikamaru belong to?", "options": ["Nara", "Akimichi", "Yamanaka", "Aburame"], "answer": "Nara", "explanation": "The Nara clan is known for shadow techniques and exceptional strategic skill.", "category": "Clans & Dojutsu"},
    {"question": "What is Haku's kekkei genkai?", "options": ["Lava Release", "Ice Release", "Wood Release", "Boil Release"], "answer": "Ice Release", "explanation": "Haku combines Water and Wind Release to use Ice Release.", "category": "Jutsu"},
    {"question": "Who gave Kakashi his Sharingan?", "options": ["Itachi", "Shisui", "Obito", "Madara"], "answer": "Obito", "explanation": "Obito Uchiha gives Kakashi his left Sharingan during the Kannabi Bridge mission.", "category": "Characters"},
    {"question": "What is the name of Kakashi's father?", "options": ["Sakumo Hatake", "Fugaku Uchiha", "Dan Kato", "Hiashi Hyuga"], "answer": "Sakumo Hatake", "explanation": "Sakumo Hatake was known across the shinobi world as Konoha's White Fang.", "category": "Characters"},
    {"question": "Which clan does Neji Hyuga belong to?", "options": ["Uchiha", "Hyuga", "Senju", "Uzumaki"], "answer": "Hyuga", "explanation": "Neji is a prodigy of the Hyuga clan's branch family.", "category": "Clans & Dojutsu"},
    {"question": "What fighting style is used by the Hyuga clan?", "options": ["Gentle Fist", "Strong Fist", "Drunken Fist", "Lightning Fist"], "answer": "Gentle Fist", "explanation": "The Hyuga use Gentle Fist to strike an opponent's chakra pathway system.", "category": "Jutsu"},
    {"question": "Where does Naruto train to become a sage?", "options": ["Mount Myoboku", "Ryuchi Cave", "Shikkotsu Forest", "Valley of the End"], "answer": "Mount Myoboku", "explanation": "Naruto learns Sage Mode at Mount Myoboku, home of the toads.", "category": "Sage Mode"},
    {"question": "Who is the jinchuriki of the Eight-Tails?", "options": ["Killer B", "Yugito Nii", "Fuu", "Roshi"], "answer": "Killer B", "explanation": "Killer B is the Eight-Tails jinchuriki and the Raikage's adopted brother.", "category": "Tailed Beasts"},
    {"question": "What is the name of the Eight-Tails?", "options": ["Gyuki", "Isobu", "Kokuo", "Chomei"], "answer": "Gyuki", "explanation": "Gyuki is the Eight-Tails sealed inside Killer B.", "category": "Tailed Beasts"},
    {"question": "Which identity does Obito use while in Akatsuki?", "options": ["Tobi", "Zetsu", "Sasori", "Kakuzu"], "answer": "Tobi", "explanation": "Obito hides behind the playful Tobi persona for much of the series.", "category": "Akatsuki"},
    {"question": "Which forbidden technique restores the dead to temporary life?", "options": ["Edo Tensei", "Izanagi", "Reaper Death Seal", "Cursed Seal"], "answer": "Edo Tensei", "explanation": "Edo Tensei, or Reanimation Jutsu, summons the souls of the deceased into living vessels.", "category": "Fourth Great Ninja War"},
    {"question": "Who originally created Edo Tensei?", "options": ["Tobirama Senju", "Orochimaru", "Kabuto Yakushi", "Hiruzen Sarutobi"], "answer": "Tobirama Senju", "explanation": "The Second Hokage, Tobirama Senju, created the Reanimation Jutsu.", "category": "Fourth Great Ninja War"},
    {"question": "Who uses Edo Tensei on a huge scale during the Fourth Great Ninja War?", "options": ["Kabuto Yakushi", "Kisame", "Danzo", "Sasori"], "answer": "Kabuto Yakushi", "explanation": "Kabuto allies with Obito and deploys a vast Edo Tensei army in the war.", "category": "Fourth Great Ninja War"},
    {"question": "Who do Naruto and Sasuke seal at the end of the Fourth Great Ninja War?", "options": ["Kaguya Otsutsuki", "Madara Uchiha", "Black Zetsu", "Hagoromo Otsutsuki"], "answer": "Kaguya Otsutsuki", "explanation": "Naruto and Sasuke use the Six Paths Chibaku Tensei to seal Kaguya.", "category": "Fourth Great Ninja War"},
    {"question": "Who is known as the Sage of Six Paths?", "options": ["Hagoromo Otsutsuki", "Hamura Otsutsuki", "Indra Otsutsuki", "Ashura Otsutsuki"], "answer": "Hagoromo Otsutsuki", "explanation": "Hagoromo Otsutsuki is the legendary Sage of Six Paths.", "category": "Lore"},
    {"question": "Which two shinobi founded Konohagakure?", "options": ["Hashirama and Madara", "Minato and Kushina", "Tobirama and Hiruzen", "Naruto and Sasuke"], "answer": "Hashirama and Madara", "explanation": "Hashirama Senju and Madara Uchiha founded the Hidden Leaf Village together.", "category": "Hidden Leaf"},
    {"question": "Who becomes the Sixth Hokage?", "options": ["Kakashi Hatake", "Danzo Shimura", "Might Guy", "Shikamaru Nara"], "answer": "Kakashi Hatake", "explanation": "Kakashi serves as Konoha's Sixth Hokage after the Fourth Great Ninja War.", "category": "Kage"},
    {"question": "Who becomes the Seventh Hokage?", "options": ["Naruto Uzumaki", "Sasuke Uchiha", "Konohamaru Sarutobi", "Shikamaru Nara"], "answer": "Naruto Uzumaki", "explanation": "Naruto fulfills his childhood dream by becoming the Seventh Hokage.", "category": "Kage"},
    {"question": "Who is Sasuke Uchiha's older brother?", "options": ["Itachi Uchiha", "Shisui Uchiha", "Obito Uchiha", "Fugaku Uchiha"], "answer": "Itachi Uchiha", "explanation": "Itachi is Sasuke's elder brother and a pivotal figure in the Uchiha tragedy.", "category": "Characters"},
    {"question": "Who is Itachi's Akatsuki partner?", "options": ["Kisame Hoshigaki", "Deidara", "Hidan", "Zetsu"], "answer": "Kisame Hoshigaki", "explanation": "Itachi and Kisame operate as an Akatsuki pair.", "category": "Akatsuki"},
    {"question": "What is the name of Kisame's living sword?", "options": ["Samehada", "Kubikiribocho", "Kiba", "Nuibari"], "answer": "Samehada", "explanation": "Samehada devours chakra and is Kisame's signature weapon.", "category": "Akatsuki"},
    {"question": "What does Deidara use to create his explosive art?", "options": ["Explosive clay", "Paper bombs", "Puppet cores", "Ink beasts"], "answer": "Explosive clay", "explanation": "Deidara molds explosive clay with the mouths in his hands.", "category": "Akatsuki"},
    {"question": "What material forms Konan's signature jutsu?", "options": ["Paper", "Sand", "Mist", "Wood"], "answer": "Paper", "explanation": "Konan can turn her body into paper and use it for offense and defense.", "category": "Akatsuki"},
    {"question": "What name does Sasuke give his team after it was called Hebi?", "options": ["Taka", "Kara", "Root", "Anbu"], "answer": "Taka", "explanation": "Sasuke renames Hebi to Taka as his goals change.", "category": "Sasuke's Journey"},
    {"question": "What is Naruto's primary chakra nature?", "options": ["Wind", "Fire", "Lightning", "Earth"], "answer": "Wind", "explanation": "Naruto's natural affinity is Wind Release, which he uses to develop the Rasenshuriken.", "category": "Jutsu"},
    {"question": "Which clan does Hinata belong to?", "options": ["Hyuga", "Inuzuka", "Uzumaki", "Senju"], "answer": "Hyuga", "explanation": "Hinata is an heiress of the Hyuga clan and a Byakugan user.", "category": "Clans & Dojutsu"},
    {"question": "Which clan is known for using insects as part of its techniques?", "options": ["Aburame", "Nara", "Akimichi", "Yamanaka"], "answer": "Aburame", "explanation": "The Aburame clan cultivates kikaichu insects that live in their bodies.", "category": "Clans & Dojutsu"},
]

ACHIEVEMENTS = {
    "first_step": ("🍥", "Genin's first step", "Complete your first mission question."),
    "on_fire": ("🔥", "Will of Fire", "Build a 3-answer correct streak."),
    "quick_thinker": ("⚡", "Yellow Flash", "Answer a question correctly in under 10 seconds."),
    "sharp_mind": ("🎯", "Chunin-level mind", "Finish a mission with 80% or more."),
    "perfect": ("👑", "Hokage's resolve", "Complete every mission perfectly."),
    "coin_collector": ("🪙", "Ryo collector", "Earn 50 ryo across this session."),
}


def inject_css():
    """Apply the game-like dark visual system."""
    st.markdown(
        """
        <style>
            :root { --ink:#fff1d2; --muted:#c7ad84; --panel:#24160f; --edge:#743b19;
                    --orange:#e86d1f; --gold:#f6c453; --leaf:#71924a; --chakra:#5ea6c8; --red:#b54431; }
            .stApp { background:
                radial-gradient(circle at 11% 5%, rgba(232,109,31,.28), transparent 27rem),
                radial-gradient(circle at 88% 16%, rgba(94,166,200,.17), transparent 24rem),
                linear-gradient(145deg,#100b08 0%,#20130d 51%,#100f0b 100%); color:var(--ink); }
            #MainMenu, footer, header { visibility: hidden; }
            .block-container { max-width: 1120px; padding-top: 2.1rem; padding-bottom: 3rem; }
            [data-testid="stSidebar"] { background:linear-gradient(180deg,#21130c 0%,#120b07 100%); border-right:1px solid var(--edge); }
            [data-testid="stSidebar"] * { color:var(--ink); }
            .hero { text-align:center; padding:2.8rem 1rem 1.2rem; animation: rise .65s ease-out both; }
            .hero-mark { font-size:4.7rem; line-height:1; filter:drop-shadow(0 0 20px rgba(232,109,31,.65)); animation:float 3s ease-in-out infinite; }
            .hero h1 { font-size:clamp(2.7rem,7vw,5.1rem); margin:.3rem 0 .35rem; letter-spacing:-.08em;
                        background:linear-gradient(90deg,#fff1d2,#f6c453 48%,#e86d1f); -webkit-background-clip:text; color:transparent; }
            .hero p { color:var(--muted); font-size:1.12rem; max-width:560px; margin:0 auto; }
            .eyebrow { color:var(--gold); text-transform:uppercase; letter-spacing:.18em; font-weight:700; font-size:.78rem; }
            .glass-card { background:linear-gradient(135deg,rgba(55,31,18,.9),rgba(29,17,11,.94));
                          border:1px solid rgba(232,109,31,.3); border-radius:22px; padding:1.45rem;
                          box-shadow:0 18px 55px rgba(0,0,0,.24); }
            .welcome-card { max-width:610px; margin:1.7rem auto; }
            .game-title { font-size:1.6rem; font-weight:800; margin:0; }
            .question-label { color:var(--muted); font-size:.9rem; margin-bottom:.5rem; }
            .question-text { font-size:clamp(1.35rem,3vw,2rem); font-weight:750; line-height:1.3; margin:.3rem 0 1.45rem; }
            .category-pill { background:rgba(246,196,83,.11); color:#ffe29a; border:1px solid rgba(246,196,83,.32);
                             padding:.28rem .72rem; border-radius:999px; font-weight:700; font-size:.78rem; display:inline-block; }
            .stat-card { border:1px solid rgba(255,255,255,.09); border-radius:15px; padding:.85rem .9rem;
                         background:rgba(255,255,255,.035); min-height:91px; }
            .stat-value { font-weight:800; font-size:1.55rem; line-height:1.25; }
            .stat-label { color:var(--muted); font-size:.76rem; text-transform:uppercase; letter-spacing:.09em; }
            .side-brand { text-align:center; font-weight:900; font-size:1.5rem; margin:.4rem 0 1.45rem; }
            .side-brand span { color:var(--orange); }
            .level-box { padding:1rem; border-radius:17px; background:linear-gradient(135deg,rgba(232,109,31,.25),rgba(246,196,83,.09)); border:1px solid rgba(232,109,31,.38); margin:.7rem 0 1rem; }
            .level-title { font-weight:800; font-size:1.08rem; }
            .level-sub { color:var(--muted); font-size:.78rem; margin-top:.18rem; }
            .summary-title { text-align:center; font-size:clamp(2.15rem,5vw,3.5rem); font-weight:900; margin:.35rem 0; }
            .grade-badge { width:105px; height:105px; border-radius:50%; display:flex; align-items:center; justify-content:center;
                           margin:1rem auto; font-size:3rem; font-weight:900; color:#261308; background:linear-gradient(135deg,var(--gold),var(--orange)); box-shadow:0 0 38px rgba(246,196,83,.3); }
            .result-copy { text-align:center; color:var(--muted); font-size:1.07rem; margin-bottom:1.1rem; }
            .achievement { padding:.78rem .9rem; border-radius:14px; background:rgba(246,196,83,.07); border:1px solid rgba(246,196,83,.2); margin:.45rem 0; }
            .achievement b { color:#ffe29a; }
            .confetti { position:fixed; inset:0; pointer-events:none; overflow:hidden; z-index:99; }
            .confetti i { position:absolute; width:10px; height:16px; opacity:.9; animation: fall 2.9s linear infinite; }
            .confetti i:nth-child(1){left:7%;background:#e86d1f;animation-delay:0s}.confetti i:nth-child(2){left:20%;background:#5ea6c8;animation-delay:.5s}.confetti i:nth-child(3){left:34%;background:#f6c453;animation-delay:1.1s}.confetti i:nth-child(4){left:50%;background:#71924a;animation-delay:.25s}.confetti i:nth-child(5){left:63%;background:#b54431;animation-delay:.85s}.confetti i:nth-child(6){left:78%;background:#e86d1f;animation-delay:1.35s}.confetti i:nth-child(7){left:92%;background:#f6c453;animation-delay:1.7s}
            .balloon { position:fixed; bottom:-92px; font-size:3.1rem; opacity:.82; pointer-events:none; animation: balloon 7s ease-in infinite; z-index:3; }
            .balloon.one { left:5%; animation-delay:0s }.balloon.two { right:8%; animation-delay:2.3s }.balloon.three { left:82%; animation-delay:4.2s }
            div.stButton > button { border:none; border-radius:12px; background:linear-gradient(100deg,#e86d1f,#b54431); color:#fff7e8; font-weight:800;
                                    padding:.66rem 1.2rem; transition:transform .18s,box-shadow .18s; }
            div.stButton > button:hover { transform:translateY(-2px); box-shadow:0 9px 25px rgba(232,109,31,.38); color:#fff7e8; }
            div[data-baseweb="radio"] label { background:rgba(255,255,255,.035); border:1px solid rgba(255,255,255,.1); padding:.55rem .75rem; border-radius:11px; margin:.35rem 0; transition:.18s; }
            div[data-baseweb="radio"] label:hover { border-color:rgba(246,196,83,.62); background:rgba(246,196,83,.06); }
            .stProgress > div > div > div > div { background:linear-gradient(90deg,#e86d1f,#f6c453); }
            @keyframes float { 50% { transform:translateY(-9px) rotate(3deg); } }
            @keyframes rise { from {opacity:0;transform:translateY(15px)} to {opacity:1;transform:none} }
            @keyframes fall { from {transform:translateY(-10vh) rotate(0deg)} to {transform:translateY(110vh) rotate(540deg)} }
            @keyframes balloon { 0% {transform:translateY(0) rotate(-3deg);opacity:0} 12% {opacity:.8} 100% {transform:translateY(-125vh) rotate(8deg);opacity:0} }
            @media(max-width:640px) { .block-container { padding-top:1.1rem; } .glass-card { padding:1rem; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state():
    defaults = {
        "screen": "welcome",
        "player_name": "",
        "questions": [],
        "question_index": 0,
        "answers": [],
        "score": 0,
        "xp": 0,
        "coins": 0,
        "current_streak": 0,
        "best_streak": 0,
        "quiz_started_at": None,
        "question_started_at": None,
        "feedback": None,
        "unlocked": set(),
        "session_xp": 0,
        "session_coins": 0,
        "quizzes_completed": 0,
        "confetti_sent": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def level_for(xp):
    """Return a shinobi rank level and the chakra XP needed for the next rank."""
    level = xp // 150 + 1
    progress = xp % 150
    return level, progress, 150


def rank_name(level):
    ranks = ("Academy student", "Genin", "Chunin", "Jonin", "ANBU", "Kage")
    return ranks[min(level - 1, len(ranks) - 1)]


def clock(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def total_elapsed():
    started = st.session_state.quiz_started_at
    return time.time() - started if started else 0


def grade_for(percentage):
    if percentage >= 90:
        return "A+", "Legendary work - your ninja way shines."
    if percentage >= 80:
        return "A", "Excellent mission work - a truly sharp result."
    if percentage >= 70:
        return "B", "Great job - your shinobi knowledge is strong."
    if percentage >= 60:
        return "C", "Mission clear - you passed and learned along the way."
    if percentage >= 50:
        return "D", "You are close - a mission debrief will make the difference."
    return "F", "Every shinobi starts somewhere. Review the scroll and train again!"


def unlock(key):
    st.session_state.unlocked.add(key)


def update_achievements_after_answer(correct, seconds_taken):
    unlock("first_step")
    if st.session_state.current_streak >= 3:
        unlock("on_fire")
    if correct and seconds_taken < 10:
        unlock("quick_thinker")
    if st.session_state.session_coins >= 50:
        unlock("coin_collector")


def start_quiz():
    # Radio widget keys are question-number based. Clear prior values so a replay
    # always begins with no answer selected.
    for key in list(st.session_state.keys()):
        if key.startswith("choice_"):
            del st.session_state[key]
    questions = random.sample(QUESTION_BANK, 20)
    st.session_state.questions = questions
    st.session_state.question_index = 0
    st.session_state.answers = []
    st.session_state.score = 0
    st.session_state.xp = 0
    st.session_state.coins = 0
    st.session_state.current_streak = 0
    st.session_state.quiz_started_at = time.time()
    st.session_state.question_started_at = time.time()
    st.session_state.feedback = None
    st.session_state.confetti_sent = False
    st.session_state.screen = "quiz"


def finish_quiz():
    total = len(st.session_state.questions)
    percentage = round((st.session_state.score / total) * 100) if total else 0
    if percentage >= 80:
        unlock("sharp_mind")
    if st.session_state.score == total:
        unlock("perfect")
    st.session_state.quizzes_completed += 1
    st.session_state.screen = "results"


def reset_to_welcome():
    for key in ["player_name", "questions", "answers", "feedback"]:
        st.session_state[key] = "" if key == "player_name" else ([] if key != "feedback" else None)
    st.session_state.screen = "welcome"
    st.session_state.confetti_sent = False


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="side-brand">SHINOBI <span>TRIALS</span></div>', unsafe_allow_html=True)
        if st.session_state.screen == "welcome":
            st.markdown("<p style='color:#c7ad84;text-align:center'>A 20-question Naruto and Shippuden mission with ranks, chakra, and rewards.</p>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("#### Mission briefing")
            st.markdown(":material/shuffle: A fresh set of 20 anime questions every run  \n:material/bolt: Fast correct answers earn bonus chakra XP  \n:material/military_tech: Unlock shinobi achievements as you play")
            return

        answered = len(st.session_state.answers)
        total = len(st.session_state.questions)
        level, progress, needed = level_for(st.session_state.xp)
        st.markdown(
            f'<div class="level-box"><div class="level-title">Rank: {rank_name(level)}</div>'
            f'<div class="level-sub">{progress} / {needed} chakra XP to {rank_name(level + 1)}</div></div>',
            unsafe_allow_html=True,
        )
        st.progress(progress / needed)
        st.markdown("#### Shinobi stats")
        left, right = st.columns(2)
        left.metric("Mission", f"{st.session_state.score}/{total}")
        right.metric("Time", clock(total_elapsed()))
        left, right = st.columns(2)
        left.metric("Chakra XP", st.session_state.xp)
        right.metric("Ryo", f"🪙 {st.session_state.coins}")
        st.metric("Best combo", f"🔥 {st.session_state.best_streak}")
        st.markdown("---")
        st.markdown(f"**Mission progress**<br>{answered} of {total} answered", unsafe_allow_html=True)
        st.progress(answered / total if total else 0)
        st.markdown("---")
        st.caption(f"Shinobi name: **{st.session_state.player_name}**")
        st.markdown("---")
        st.markdown("OK -Yellow Flash Of the Leaf")


def render_welcome():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-mark">🍥</div>
            <div class="eyebrow">The will of fire</div>
            <h1>Shinobi Trials</h1>
            <p>Twenty Naruto and Shippuden questions. Build chakra, earn ryo, and rise through the ranks.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="glass-card welcome-card">', unsafe_allow_html=True)
    st.markdown("### Ready, shinobi?")
    st.caption("Enter your shinobi name to accept the mission. Spoilers cover Naruto and Shippuden.")
    name = st.text_input("Shinobi name", value=st.session_state.player_name, placeholder="e.g. Kakashi Hatake", max_chars=30)
    st.caption("Use 2-30 letters; spaces, apostrophes, and hyphens are welcome.")
    if st.button("Accept mission", icon=":material/play_arrow:", width="stretch"):
        clean_name = name.strip()
        if not re.fullmatch(r"[A-Za-z][A-Za-z '\\-]{1,29}", clean_name):
            st.error("Enter a valid shinobi name with at least 2 letters.", icon=":material/error:")
        else:
            st.session_state.player_name = clean_name
            start_quiz()
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    a, b, c = st.columns(3)
    for col, icon, title, text in [
        (a, "🍃", "20 mission questions", "A new random mix from across the full anime."),
        (b, "⚡", "Build chakra", "Fast, correct answers earn bonus chakra XP and ryo."),
        (c, "🏆", "Rise through ranks", "Unlock achievements and chase a Hokage-level run."),
    ]:
        with col:
            st.markdown(f'<div class="stat-card"><div style="font-size:1.55rem">{icon}</div><b>{title}</b><br><span style="color:#a8abc6;font-size:.86rem">{text}</span></div>', unsafe_allow_html=True)


def render_quiz():
    index = st.session_state.question_index
    questions = st.session_state.questions
    if index >= len(questions):
        finish_quiz()
        st.rerun()

    question = questions[index]
    total = len(questions)
    st.markdown(f'<div class="balloon one">🎈</div><div class="balloon two">🎈</div><div class="balloon three">🎈</div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Quest in progress</div>', unsafe_allow_html=True)
    header_left, header_right = st.columns([5, 1])
    with header_left:
        st.markdown(f'<p class="game-title">Question {index + 1} <span style="color:#a8abc6;font-size:1rem">of {total}</span></p>', unsafe_allow_html=True)
    with header_right:
        st.markdown(f'<div style="text-align:right;padding-top:.25rem"><span class="category-pill">{question["category"]}</span></div>', unsafe_allow_html=True)
    st.progress(index / total)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="question-label">Choose the best answer</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="question-text">{question["question"]}</div>', unsafe_allow_html=True)

    if st.session_state.feedback is None:
        choice = st.radio(
            "Answer",
            question["options"],
            index=None,
            key=f"choice_{index}",
            label_visibility="collapsed",
        )
        if st.button("Lock in answer", type="primary", use_container_width=True):
            if choice is None:
                st.warning("Pick an answer before locking it in.")
            else:
                seconds_taken = time.time() - st.session_state.question_started_at
                correct = choice == question["answer"]
                xp_earned = 0
                coins_earned = 0
                if correct:
                    speed_bonus = 10 if seconds_taken < 10 else (5 if seconds_taken < 20 else 0)
                    xp_earned = 25 + speed_bonus
                    coins_earned = 5 + (2 if seconds_taken < 10 else 0)
                    st.session_state.score += 1
                    st.session_state.xp += xp_earned
                    st.session_state.session_xp += xp_earned
                    st.session_state.coins += coins_earned
                    st.session_state.session_coins += coins_earned
                    st.session_state.current_streak += 1
                    st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.current_streak)
                else:
                    st.session_state.current_streak = 0
                st.session_state.answers.append(
                    {
                        "question": question["question"],
                        "category": question["category"],
                        "selected": choice,
                        "correct_answer": question["answer"],
                        "explanation": question["explanation"],
                        "correct": correct,
                        "seconds": seconds_taken,
                        "xp": xp_earned,
                        "coins": coins_earned,
                    }
                )
                update_achievements_after_answer(correct, seconds_taken)
                st.session_state.feedback = {"correct": correct, "xp": xp_earned, "coins": coins_earned}
                st.rerun()
    else:
        feedback = st.session_state.feedback
        if feedback["correct"]:
            st.success(f"Correct! +{feedback['xp']} XP  •  +{feedback['coins']} coins")
        else:
            st.error(f"Not quite — the correct answer is **{question['answer']}**.")
        st.info(f"💡 **Why?** {question['explanation']}")
        if st.session_state.current_streak >= 2 and feedback["correct"]:
            st.markdown(f"<p style='color:#ffd166;font-weight:800'>🔥 {st.session_state.current_streak}-answer streak!</p>", unsafe_allow_html=True)
        next_label = "See my results  →" if index == total - 1 else "Next question  →"
        if st.button(next_label, type="primary", use_container_width=True):
            st.session_state.question_index += 1
            st.session_state.question_started_at = time.time()
            st.session_state.feedback = None
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_results():
    total = len(st.session_state.questions)
    score = st.session_state.score
    percentage = round(score / total * 100) if total else 0
    grade, message = grade_for(percentage)
    passed = percentage >= 60
    level, _, _ = level_for(st.session_state.xp)

    if not st.session_state.confetti_sent:
        st.balloons()
        st.session_state.confetti_sent = True
    st.markdown('<div class="confetti"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero" style="padding-bottom:.2rem"><div class="hero-mark">🏁</div><div class="eyebrow">Quest complete</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="summary-title">{message}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="grade-badge">{grade}</div>', unsafe_allow_html=True)
    status_color = "#45e4a6" if passed else "#ff70b8"
    status_label = "PASS" if passed else "KEEP PRACTICING"
    st.markdown(
        f'<div class="result-copy">{st.session_state.player_name}, you scored '
        f'<b style="color:#fff">{score}/{total}</b> ({percentage}%) — '
        f'<b style="color:{status_color}">{status_label}</b></div>',
        unsafe_allow_html=True,
    )

    s1, s2, s3, s4 = st.columns(4)
    stats = [(s1, "Correct", f"{score}/{total}"), (s2, "Time", clock(total_elapsed())), (s3, "Earned", f"{st.session_state.xp} XP"), (s4, "Level", f"{level} Explorer")]
    for column, label, value in stats:
        with column:
            st.markdown(f'<div class="stat-card"><div class="stat-label">{label}</div><div class="stat-value">{value}</div></div>', unsafe_allow_html=True)

    st.markdown("### Achievements unlocked")
    unlocked = st.session_state.unlocked
    if unlocked:
        cols = st.columns(2)
        for position, key in enumerate(sorted(unlocked)):
            icon, title, description = ACHIEVEMENTS[key]
            with cols[position % 2]:
                st.markdown(f'<div class="achievement">{icon} <b>{title}</b><br><span style="color:#a8abc6;font-size:.87rem">{description}</span></div>', unsafe_allow_html=True)
    else:
        st.caption("Your next run can unlock the first one.")

    st.markdown("### Answer review")
    for number, answer in enumerate(st.session_state.answers, 1):
        symbol = "✅" if answer["correct"] else "❌"
        with st.expander(f"{symbol} {number}. {answer['question']}"):
            st.markdown(f"**Your answer:** {answer['selected']}")
            st.markdown(f"**Correct answer:** {answer['correct_answer']}")
            st.markdown(f"💡 {answer['explanation']}")
            st.caption(f"{answer['category']} · {answer['seconds']:.1f}s · +{answer['xp']} XP · +{answer['coins']} coins")

    left, right = st.columns(2)
    with left:
        if st.button("Play another random quest  ↻", type="primary", use_container_width=True):
            start_quiz()
            st.rerun()
    with right:
        if st.button("Change player", use_container_width=True):
            reset_to_welcome()
            st.rerun()


def main():
    inject_css()
    init_state()
    render_sidebar()
    if st.session_state.screen == "welcome":
        render_welcome()
    elif st.session_state.screen == "quiz":
        render_quiz()
    else:
        render_results()


if __name__ == "__main__":
    main()
