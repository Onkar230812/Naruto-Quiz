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

  # Expanded Naruto and Naruto Shippuden question bank (150+ Questions)
QUESTION_BANK = [
    # --- HIDDEN LEAF / LORE (30 Questions) ---
    {"question": "What is the title given to the leader of Konohagakure?", "options": ["Kazekage", "Hokage", "Mizukage", "Raikage"], "answer": "Hokage", "explanation": "The Hokage is the leader of the Hidden Leaf Village.", "category": "Hidden Leaf"},
    {"question": "Which two shinobi founded Konohagakure?", "options": ["Hashirama and Madara", "Minato and Kushina", "Tobirama and Hiruzen", "Naruto and Sasuke"], "answer": "Hashirama and Madara", "explanation": "Hashirama Senju and Madara Uchiha founded the Hidden Leaf Village together.", "category": "Hidden Leaf"},
    {"question": "What does the symbol on Konoha's headbands represent?", "options": ["A leaf", "A whirlpool", "A fire flame", "A bird wing"], "answer": "A leaf", "explanation": "The stylized symbol represents a leaf, symbolizing the Hidden Leaf Village.", "category": "Hidden Leaf"},
    {"question": "Who was the Second Hokage of Konoha?", "options": ["Tobirama Senju", "Hashirama Senju", "Hiruzen Sarutobi", "Minato Namikaze"], "answer": "Tobirama Senju", "explanation": "Tobirama Senju succeeded his brother Hashirama to become the Second Hokage.", "category": "Hidden Leaf"},
    {"question": "Who was the Third Hokage of Konoha?", "options": ["Hiruzen Sarutobi", "Tobirama Senju", "Danzo Shimura", "Jiraiya"], "answer": "Hiruzen Sarutobi", "explanation": "Hiruzen Sarutobi was the Third Hokage, known as the Professor.", "category": "Hidden Leaf"},
    {"question": "Who becomes the Fifth Hokage?", "options": ["Tsunade", "Kurenai", "Anko", "Temari"], "answer": "Tsunade", "explanation": "Tsunade returns to Konoha and becomes its Fifth Hokage.", "category": "Hidden Leaf"},
    {"question": "Who becomes the Sixth Hokage?", "options": ["Kakashi Hatake", "Danzo Shimura", "Might Guy", "Shikamaru Nara"], "answer": "Kakashi Hatake", "explanation": "Kakashi serves as Konoha's Sixth Hokage after the Fourth Great Ninja War.", "category": "Hidden Leaf"},
    {"question": "Who becomes the Seventh Hokage?", "options": ["Naruto Uzumaki", "Sasuke Uchiha", "Konohamaru Sarutobi", "Shikamaru Nara"], "answer": "Naruto Uzumaki", "explanation": "Naruto fulfills his childhood dream by becoming the Seventh Hokage.", "category": "Hidden Leaf"},
    {"question": "What is the name of the store where Naruto eats ramen?", "options": ["Ichiraku Ramen", "Shio Ramen", "Konoha Noodle House", "Naruto Toppings"], "answer": "Ichiraku Ramen", "explanation": "Teuchi and Ayame run Naruto's favorite restaurant, Ichiraku Ramen.", "category": "Hidden Leaf"},
    {"question": "Who was the leader of the Foundation (Root) sub-division of ANBU?", "options": ["Danzo Shimura", "Hiruzen Sarutobi", "Sai", "Kakashi Hatake"], "answer": "Danzo Shimura", "explanation": "Danzo Shimura founded and led the extremist, underground faction known as Root.", "category": "Hidden Leaf"},
    {"question": "Which monument dominates the landscape behind the Hokage office?", "options": ["Hokage Rock", "Valley of the End", "Tanzaku Castle", "Naka Shrine"], "answer": "Hokage Rock", "explanation": "Hokage Rock features the stone-carved faces of all presiding Hokage.", "category": "Hidden Leaf"},
    {"question": "What is the primary currency used across the shinobi nations?", "options": ["Ryo", "Yen", "Chakra Stone", "Gold Bars"], "answer": "Ryo", "explanation": "Ryo is the universal monetary system utilized throughout the ninja world.", "category": "Lore"},
    {"question": "Who is known as the Sage of Six Paths?", "options": ["Hagoromo Otsutsuki", "Hamura Otsutsuki", "Indra Otsutsuki", "Ashura Otsutsuki"], "answer": "Hagoromo Otsutsuki", "explanation": "Hagoromo Otsutsuki is the legendary Sage of Six Paths.", "category": "Lore"},
    {"question": "Who was the biological ancestor of the Uchiha Clan?", "options": ["Indra Otsutsuki", "Ashura Otsutsuki", "Hamura Otsutsuki", "Kaguya Otsutsuki"], "answer": "Indra Otsutsuki", "explanation": "Indra, the elder son of Hagoromo, inherited his visual powers and fathered the Uchiha ancestry.", "category": "Lore"},
    {"question": "Who was the biological ancestor of the Senju and Uzumaki Clans?", "options": ["Ashura Otsutsuki", "Indra Otsutsuki", "Kaguya Otsutsuki", "Black Zetsu"], "answer": "Ashura Otsutsuki", "explanation": "Ashura, the younger son of Hagoromo, passed down his physical vitality to the Senju and Uzumaki lines.", "category": "Lore"},
    {"question": "What is the true origin of all chakra on Earth?", "options": ["The God Tree", "The Toad Sage", "The Grim Reaper", "The Death God Seal"], "answer": "The God Tree", "explanation": "Chakra originates from the God Tree, whose fruit was consumed by Kaguya Otsutsuki.", "category": "Lore"},
    {"question": "What was the name of the ancient era before hidden villages were formed?", "options": ["Warring States Period", "Feudal Chaos Era", "Great Shinobi Dawn", "Pre-Chakra Dynasty"], "answer": "Warring States Period", "explanation": "The Warring States Period consisted of independent mercenary clans constantly fighting each other.", "category": "Lore"},
    {"question": "Which clan was completely slaughtered to prevent a coup d'état in Konoha?", "options": ["Uchiha Clan", "Hyuga Clan", "Senju Clan", "Uzumaki Clan"], "answer": "Uchiha Clan", "explanation": "Itachi Uchiha massacred the Uchiha clan to avoid a destructive civil uprising.", "category": "Lore"},
    {"question": "What happened to Uzushio, the Hidden Whirlpool Village?", "options": ["Destroyed by rival nations", "Sunk by an earthquake", "Abandoned due to famine", "Merged into Konoha"], "answer": "Destroyed by rival nations", "explanation": "Other nations destroyed Uzushio because they feared the village's devastating sealing jutsu capabilities.", "category": "Lore"},
    {"question": "What custom badge do Konoha ninja wear on the back of their flak jackets?", "options": ["The Uzumaki Crest", "The Senju Leaf", "A Flame Emblem", "A Shuriken Mark"], "answer": "The Uzumaki Crest", "explanation": "Konoha displays the red Uzumaki whirlpool emblem on uniforms to honor their historic alliance.", "category": "Hidden Leaf"},
    {"question": "What is the name of Konoha's forest used for the Chunin Exams?", "options": ["Forest of Death", "Whispering Woods", "Chakra Jungle", "The Dead Zone"], "answer": "Forest of Death", "explanation": "The 44th Training Ground is notoriously called the Forest of Death.", "category": "Hidden Leaf"},
    {"question": "Who served as the principal proctor for the first stage of the Chunin Exams?", "options": ["Ibiki Morino", "Anko Mitarashi", "Genma Shiranui", "Hayate Gekko"], "answer": "Ibiki Morino", "explanation": "Ibiki Morino, an interrogation specialist, proctored the grueling written exam stage.", "category": "Hidden Leaf"},
    {"question": "Which bridge did Team 7 protect during their first major C-rank mission?", "options": ["The Great Naruto Bridge", "The Kannabi Bridge", "The Tenchi Bridge", "The Samurai Bridge"], "answer": "The Great Naruto Bridge", "explanation": "Tazuna named the bridge 'The Great Naruto Bridge' to inspire the land of Waves.", "category": "Lore"},
    {"question": "Which historical landmark is the site of Naruto and Sasuke's major duels?", "options": ["Valley of the End", "Final Rest Basin", "Founders Canyon", "Waterfall of Truth"], "answer": "Valley of the End", "explanation": "The Valley of the End features massive stone statues of Hashirama and Madara.", "category": "Lore"},
    {"question": "What is the name of the traditional gathering spot for Team Asuma?", "options": ["Yakiniku Q", "Dango Shop", "Ichiraku", "Sweet Bean Cafe"], "answer": "Yakiniku Q", "explanation": "Team Asuma regularly celebrates or debriefs over BBQ at Yakiniku Q.", "category": "Hidden Leaf"},
    {"question": "Which Hokage created the Ninja Academy and the Chunin Exam structure?", "options": ["Tobirama Senju", "Hashirama Senju", "Hiruzen Sarutobi", "Minato Namikaze"], "answer": "Tobirama Senju", "explanation": "Tobirama developed most of Konoha's institutions, including the Academy, ANBU, and Exams.", "category": "Hidden Leaf"},
    {"question": "What special position did Dan Kato dream of achieving before he died?", "options": ["Hokage", "ANBU Captain", "12 Guardian Ninja", "Medical Corps Head"], "answer": "Hokage", "explanation": "Tsunade's lover Dan Kato shared Naruto's dream of becoming Hokage before dying in battle.", "category": "Lore"},
    {"question": "Who was the original founder of the Akatsuki in Amegakure?", "options": ["Yahiko", "Nagato", "Obito", "Konan"], "answer": "Yahiko", "explanation": "Yahiko founded the original Akatsuki alongside Nagato and Konan to achieve peace.", "category": "Lore"},
    {"question": "Who engineered the plan to cast the Infinite Tsukuyomi over thousands of years?", "options": ["Black Zetsu", "Madara Uchiha", "Obito Uchiha", "Kaguya Otsutsuki"], "answer": "Black Zetsu", "explanation": "Black Zetsu manipulated generations of Indra's descendants to revive Kaguya.", "category": "Lore"},
    {"question": "Which village is hidden behind walls of steep mountains and rocks?", "options": ["Iwagakure", "Sunagakure", "Kirigakure", "Kumogakure"], "answer": "Iwagakure", "explanation": "Iwagakure is the Hidden Stone Village, naturally guarded by massive rocky terrain.", "category": "Lore"},

    # --- CHARACTERS (30 Questions) ---
    {"question": "Who is Naruto Uzumaki's father?", "options": ["Jiraiya", "Minato Namikaze", "Hiruzen Sarutobi", "Kakashi Hatake"], "answer": "Minato Namikaze", "explanation": "Minato Namikaze, the Fourth Hokage, is Naruto's father.", "category": "Characters"},
    {"question": "Who is Naruto Uzumaki's mother?", "options": ["Tsunade", "Mikoto Uchiha", "Kushina Uzumaki", "Konan"], "answer": "Kushina Uzumaki", "explanation": "Kushina Uzumaki was Naruto's mother and the previous Nine-Tails jinchuriki.", "category": "Characters"},
    {"question": "Who is Sasuke Uchiha's older brother?", "options": ["Itachi Uchiha", "Shisui Uchiha", "Obito Uchiha", "Fugaku Uchiha"], "answer": "Itachi Uchiha", "explanation": "Itachi is Sasuke's elder brother and a pivotal figure in the Uchiha tragedy.", "category": "Characters"},
    {"question": "Who gave Kakashi his Sharingan?", "options": ["Itachi", "Shisui", "Obito", "Madara"], "answer": "Obito", "explanation": "Obito Uchiha gives Kakashi his left Sharingan during the Kannabi Bridge mission.", "category": "Characters"},
    {"question": "What is the name of Kakashi's father?", "options": ["Sakumo Hatake", "Fugaku Uchiha", "Dan Kato", "Hiashi Hyuga"], "answer": "Sakumo Hatake", "explanation": "Sakumo Hatake was known across the shinobi world as Konoha's White Fang.", "category": "Characters"},
    {"question": "What nickname was given to Minato Namikaze due to his extreme speed?", "options": ["The Yellow Flash", "The White Fang", "The Lightning Blade", "The Golden Shadow"], "answer": "The Yellow Flash", "explanation": "Minato was internationally feared as 'The Yellow Flash of the Leaf'.", "category": "Characters"},
    {"question": "What is the name of Tsunade's younger brother who died in childhood?", "options": ["Nawaki", "Dan", "Kizashi", "Iruka"], "answer": "Nawaki", "explanation": "Nawaki died in battle right after receiving his grandmother's first Hokage necklace.", "category": "Characters"},
    {"question": "What is Tsunade's primary addiction or vice?", "options": ["Gambling", "Drinking", "Shopping", "Sleeping"], "answer": "Gambling", "explanation": "Tsunade is a compulsive gambler, notoriously known as 'The Legendary Sucker' due to her terrible luck.", "category": "Characters"},
    {"question": "Who is Konohamaru's grandfather?", "options": ["Hiruzen Sarutobi", "Asuma Sarutobi", "Danzo Shimura", "Homura Mitokado"], "answer": "Hiruzen Sarutobi", "explanation": "Konohamaru is the direct grandson of the Third Hokage, Hiruzen Sarutobi.", "category": "Characters"},
    {"question": "Which member of the Legendary Sannin left Konoha to build the Hidden Sound Village?", "options": ["Orochimaru", "Jiraiya", "Tsunade", "Hanzo"], "answer": "Orochimaru", "explanation": "Orochimaru defected from Konoha to pursue immortality and founded Otogakure.", "category": "Characters"},
    {"question": "Who is the grandson of Hashirama Senju?", "options": ["Nawaki", "Yamato", "Sai", "Dan"], "answer": "Nawaki", "explanation": "Nawaki and Tsunade are the direct grandchildren of Hashirama Senju.", "category": "Characters"},
    {"question": "What is the name of Sasuke Uchiha's mother?", "options": ["Mikoto Uchiha", "Kushina Uzumaki", "Karui", "Mebuki Haruno"], "answer": "Mikoto Uchiha", "explanation": "Mikoto Uchiha was the mother of Itachi and Sasuke Uchiha.", "category": "Characters"},
    {"question": "What is the name of Sasuke Uchiha's father?", "options": ["Fugaku Uchiha", "Madara Uchiha", "Tajima Uchiha", "Shisui Uchiha"], "answer": "Fugaku Uchiha", "explanation": "Fugaku Uchiha was the head of the Uchiha clan and the Konoha Military Police.", "category": "Characters"},
    {"question": "Which character possesses a running gag of getting lost and giving terrible excuses?", "options": ["Kakashi Hatake", "Obito Uchiha", "Jiraiya", "Naruto Uzumaki"], "answer": "Kakashi Hatake", "explanation": "Kakashi frequently shows up late to team meetings, adopting Obito's old habit of making up absurd excuses.", "category": "Characters"},
    {"question": "What is the full name of the shopkeeper who runs Ichiraku Ramen?", "options": ["Teuchi", "Choji", "Sukeru", "Ayame"], "answer": "Teuchi", "explanation": "Teuchi is the owner and master chef of Ichiraku Ramen.", "category": "Characters"},
    {"question": "Who is Teuchi's daughter who works alongside him at Ichiraku?", "options": ["Ayame", "Tenten", "Matsuri", "Moegi"], "answer": "Ayame", "explanation": "Ayame works as a waitress and cook at Ichiraku Ramen with her father.", "category": "Characters"},
    {"question": "Who was Kakashi's rival and best friend who fought using Nunchaku?", "options": ["Might Guy", "Asuma Sarutobi", "Ibiki Morino", "Aoba Yamashiro"], "answer": "Might Guy", "explanation": "Might Guy considers himself Kakashi's eternal rival and primary best friend.", "category": "Characters"},
    {"question": "Who was the biological mother of Gaara?", "options": ["Karura", "Temari", "Chiyo", "Pakura"], "answer": "Karura", "explanation": "Karura died shortly after giving birth to Gaara, infusing her love into his sand protector.", "category": "Characters"},
    {"question": "Who was Gaara's maternal uncle and primary caretaker who tried to assassinate him?", "options": ["Yashamaru", "Rasa", "Baki", "Kankuro"], "answer": "Yashamaru", "explanation": "Rasa ordered Yashamaru to test Gaara's control over the One-Tails by attacking him.", "category": "Characters"},
    {"question": "What was the name of the Fourth Kazekage, Gaara's father?", "options": ["Rasa", "Gaara", "Retto", "Shamon"], "answer": "Rasa", "explanation": "Rasa was the Fourth Kazekage who used Gold Dust in battle.", "category": "Characters"},
    {"question": "Which Akatsuki member killed Gaara's father, Rasa?", "options": ["Orochimaru", "Sasori", "Deidara", "Itachi"], "answer": "Orochimaru", "explanation": "Orochimaru assassinated Rasa right before infiltrating the Chunin Exams disguised as the Kazekage.", "category": "Characters"},
    {"question": "Who was Sai's adoptive older brother whose death caused Sai to lose his emotions?", "options": ["Shin", "Dan", "Torune", "Fu"], "answer": "Shin", "explanation": "Shin was a fellow Root member whom Sai viewed as his beloved brother.", "category": "Characters"},
    {"question": "What is the real name of the Leaf shinobi code-named Yamato?", "options": ["Tenzo", "Sai", "Yamato", "Kino"], "answer": "Tenzo", "explanation": "Kakashi frequently refers to Yamato by his original real name, Tenzo.", "category": "Characters"},
    {"question": "Which ANBU member uses crystal jutsu and looked after Kimimaro?", "options": ["Guren", "Tayuya", "Karin", "Anko"], "answer": "Guren", "explanation": "Guren was a loyal follower of Orochimaru who possessed the rare Crystal Release kekkei genkai.", "category": "Characters"},
    {"question": "Who was the leader of the Sound Four team?", "options": ["Sakon/Ukon", "Jirobo", "Kidomaru", "Tayuya"], "answer": "Sakon/Ukon", "explanation": "Sakon and his twin Ukon acted as the frontline leaders of the Sound Four.", "category": "Characters"},
    {"question": "Which clan does Kimimaro belong to?", "options": ["Kaguya Clan", "Uchiha Clan", "Yuki Clan", "Hozuki Clan"], "answer": "Kaguya Clan", "explanation": "Kimimaro was the sole survivor of the battle-hungry Kaguya clan.", "category": "Characters"},
    {"question": "Who was the older brother of Sai's teammate, Shin, in Root?", "options": ["Sai", "Shin had no brother", "Danzo", "Hyuga member"], "answer": "Sai", "explanation": "Sai was adopted into the same Root group and became Shin's surrogate brother.", "category": "Characters"},
    {"question": "Which character loves tracking down bounty rewards and carries a massive executioner blade?", "options": ["Zabuza Momochi", "Suigetsu Hozuki", "Kisame Hoshigaki", "Mangetsu Hozuki"], "answer": "Zabuza Momochi", "explanation": "Zabuza was an outlaw mercenary who carried Kubikiribocho, the Executioner's Blade.", "category": "Characters"},
    {"question": "What is the name of Zabuza's custom talking tracking dogs summoned by Kakashi?", "options": ["Ninken", "Akamaru", "Kuromaru", "Chamaru"], "answer": "Ninken", "explanation": "Kakashi's eight pack of tracking hounds are collectively known as the Ninken.", "category": "Characters"},
    {"question": "Which of Kakashi's Ninken is the smallest and sits on Naruto's head?", "options": ["Pakkun", "Bull", "Shiba", "Bisuke"], "answer": "Pakkun", "explanation": "Pakkun is the miniature pug who leads Kakashi's summoning pack.", "category": "Characters"},

    # --- TEAMS & VILLAGES (25 Questions) ---
    {"question": "Who are Naruto's teammates on Team 7?", "options": ["Sakura and Sasuke", "Neji and Rock Lee", "Shino and Kiba", "Choji and Shikamaru"], "answer": "Sakura and Sasuke", "explanation": "Team 7 begins with Naruto, Sakura Haruno, and Sasuke Uchiha under Kakashi.", "category": "Teams"},
    {"question": "Who temporarily leads Team 7 during Kakashi's absence in Shippuden?", "options": ["Yamato", "Guy", "Asuma", "Iruka"], "answer": "Yamato", "explanation": "Yamato joins Team 7 and helps contain Naruto's Nine-Tails chakra.", "category": "Teams"},
    {"question": "What is the name of Gaara's village?", "options": ["Hidden Mist", "Hidden Stone", "Hidden Sand", "Hidden Cloud"], "answer": "Hidden Sand", "explanation": "Gaara is a shinobi of Sunagakure, the Hidden Sand Village.", "category": "Villages"},
    {"question": "Which team consists of Shikamaru, Ino, and Choji?", "options": ["Team 10", "Team 8", "Team 3", "Team 5"], "answer": "Team 10", "explanation": "Asuma Sarutobi leads the historical Ino-Shika-Cho trio on Team 10.", "category": "Teams"},
    {"question": "Who is the sensei of Team 8 (Kiba, Shino, Hinata)?", "options": ["Kurenai Yuhi", "Asuma Sarutobi", "Might Guy", "Kakashi Hatake"], "answer": "Kurenai Yuhi", "explanation": "Kurenai Yuhi is the genin master of Team 8, specializing in genjutsu.", "category": "Teams"},
    {"question": "Which three genin make up Team Guy?", "options": ["Neji, Tenten, Rock Lee", "Naruto, Sakura, Sasuke", "Kiba, Shino, Hinata", "Ino, Shika, Choji"], "answer": "Neji, Tenten, Rock Lee", "explanation": "Might Guy guides the older genin team of Neji, Tenten, and Rock Lee.", "category": "Teams"},
    {"question": "What historical name is given to the formation of the Nara, Yamanaka, and Akimichi clans?", "options": ["Ino-Shika-Cho", "The Leaf Trinity", "The Shadow-Mind-Body Trio", "The Sarutobi Vanguard"], "answer": "Ino-Shika-Cho", "explanation": "The Ino-Shika-Cho combination has been maintained across multiple generations.", "category": "Teams"},
    {"question": "What is the nickname of the Hidden Mist Village due to its bloody graduation rituals?", "options": ["Village of the Bloody Mist", "Dark Fog Outpost", "The Crimson Sea", "The Slasher Village"], "answer": "Village of the Bloody Mist", "explanation": "Kirigakure was called the Bloody Mist because students had to kill classmates to graduate.", "category": "Villages"},
    {"question": "Which elite squad protects the Daimyo (Feudal Lord) of the Land of Fire?", "options": ["Twelve Guardian Ninja", "ANBU Black Ops", "The Hokage Vanguard", "Root Foundation"], "answer": "Twelve Guardian Ninja", "explanation": "Asuma Sarutobi was a former member of the prestigious Twelve Guardian Ninja.", "category": "Teams"},
    {"question": "Who is the leader of the Hidden Rain Village before being overthrown by Pain?", "options": ["Hanzo of the Salamander", "Mifune", "Churo", "Kandachi"], "answer": "Hanzo of the Salamander", "explanation": "Hanzo was the absolute ruler of the Hidden Rain Village before Pain killed him.", "category": "Villages"},
    {"question": "What is the name of the iron-clad nation ruled by Samurai rather than Ninja?", "options": ["Land of Iron", "Land of Wolves", "The Steel Citadel", "The Frost Summit"], "answer": "Land of Iron", "explanation": "The Land of Iron is a neutral territory populated entirely by heavily armored Samurai.", "category": "Villages"},
    {"question": "Which country does the Hidden Cloud Village belong to?", "options": ["Land of Lightning", "Land of Earth", "Land of Water", "Land of Wind"], "answer": "Land of Lightning", "explanation": "Kumogakure (Hidden Cloud) is located inside the rugged Land of Lightning.", "category": "Villages"},
    {"question": "Which country does the Hidden Stone Village belong to?", "options": ["Land of Earth", "Land of Lightning", "Land of Fire", "Land of Iron"], "answer": "Land of Earth", "explanation": "Iwagakure is the military stronghold of the massive Land of Earth.", "category": "Villages"},
    {"question": "Who was the sensei of Minato Namikaze?", "options": ["Jiraiya", "Hiruzen Sarutobi", "Hashirama Senju", "Kakashi Hatake"], "answer": "Jiraiya", "explanation": "Jiraiya trained Minato, who later went on to become the Fourth Hokage.", "category": "Teams"},
    {"question": "Who were Minato Namikaze's three students on his genin squad?", "options": ["Kakashi, Obito, Rin", "Naruto, Sasuke, Sakura", "Yahiko, Nagato, Konan", "Jiraiya, Tsunade, Orochimaru"], "answer": "Kakashi, Obito, Rin", "explanation": "Minato led Team Minato, consisting of Kakashi Hatake, Obito Uchiha, and Rin Nohara.", "category": "Teams"},
    {"question": "Who were the members of the original Legendary Sannin trio?", "options": ["Jiraiya, Tsunade, Orochimaru", "Minato, Kakashi, Obito", "Yahiko, Nagato, Konan", "Hashirama, Tobirama, Madara"], "answer": "Jiraiya, Tsunade, Orochimaru", "explanation": "Jiraiya, Tsunade, and Orochimaru were named the Sannin by Hanzo during the Second Ninja War.", "category": "Teams"},
    {"question": "Which village utilizes specialized puppets and giant iron fans in battle?", "options": ["Hidden Sand", "Hidden Mist", "Hidden Cloud", "Hidden Sound"], "answer": "Hidden Sand", "explanation": "Sunagakure ninja like Chiyo, Sasori, and Temari specialize in puppetry and wind tools.", "category": "Villages"},
    {"question": "What special tracking squad does Kiba Inuzuka's family run in Konoha?", "options": ["Military Police Force", "Konoha Barrier Corps", "Analysis Division", "None of these"], "answer": "None of these", "explanation": "The Uchiha ran the Police Force, while the Inuzuka are standard sensory combat specialists.", "category": "Teams"},
    {"question": "What is the name of the custom strike squad Sasuke forms to hunt Itachi?", "options": ["Hebi", "Taka", "Akatsuki", "Kara"], "answer": "Hebi", "explanation": "Sasuke initially names his rogue gathering squad Hebi (Snake) before renaming it Taka (Hawk).", "category": "Teams"},
    {"question": "What name does Sasuke give his team after it was called Hebi?", "options": ["Taka", "Kara", "Root", "Anbu"], "answer": "Taka", "explanation": "Sasuke renames Hebi to Taka as his goals change.", "category": "Teams"},
    {"question": "Who are the four members of Sasuke's team, Taka?", "options": ["Sasuke, Suigetsu, Karin, Jugo", "Sasuke, Sakura, Naruto, Kakashi", "Sasuke, Itachi, Kisame, Tobi", "Sasuke, Orochimaru, Kabuto, Kimimaro"], "answer": "Sasuke, Suigetsu, Karin, Jugo", "explanation": "Taka consists of Sasuke along with experimental rogue projects Suigetsu, Karin, and Jugo.", "category": "Teams"},
    {"question": "Which hidden village was built entirely underground by Orochimaru?", "options": ["Hidden Sound", "Hidden Hot Springs", "Hidden Shadow", "Hidden Craft"], "answer": "Hidden Sound", "explanation": "Otogakure (Hidden Sound) was Orochimaru's personal collection of secret hideouts.", "category": "Villages"},
    {"question": "Who was the sensei of the legendary Ame Orphans (Yahiko, Nagato, Konan)?", "options": ["Jiraiya", "Orochimaru", "Tsunade", "Hanzo"], "answer": "Jiraiya", "explanation": "Jiraiya stayed behind in the Hidden Rain to look after and train the orphans.", "category": "Teams"},
    {"question": "Which unit is responsible for handling internal village security and tracking rogue ninja?", "options": ["ANBU Black Ops", "Genin Guard", "Chunin Academy Police", "Medical Corps"], "answer": "ANBU Black Ops", "explanation": "The ANBU handle high-risk black ops covert actions and assassination tracking.", "category": "Teams"},
    {"question": "Which village is known for producing the Seven Ninja Swordsmen?", "options": ["Hidden Mist", "Hidden Waterfall", "Hidden Stone", "Hidden Grass"], "answer": "Hidden Mist", "explanation": "The Seven Ninja Swordsmen of the Mist are an elite group of weapons masters from Kirigakure.", "category": "Villages"},

    # --- CLANS & DOJUSTSU (25 Questions) ---
    {"question": "Which dojutsu is inherited by the Uchiha clan?", "options": ["Byakugan", "Rinnegan", "Sharingan", "Tenseigan"], "answer": "Sharingan", "explanation": "The Sharingan is the Uchiha clan's signature visual jutsu.", "category": "Clans & Dojutsu"},
    {"question": "Which clan does Neji Hyuga belong to?", "options": ["Uchiha", "Hyuga", "Senju", "Uzumaki"], "answer": "Hyuga", "explanation": "Neji is a prodigy of the Hyuga clan's branch family.", "category": "Clans & Dojutsu"},
    {"question": "Which clan does Hinata belong to?", "options": ["Hyuga", "Inuzuka", "Uzumaki", "Senju"], "answer": "Hyuga", "explanation": "Hinata is an heiress of the Hyuga clan and a Byakugan user.", "category": "Clans & Dojutsu"},
    {"question": "Which clan is known for using insects as part of its techniques?", "options": ["Aburame", "Nara", "Akimichi", "Yamanaka"], "answer": "Aburame", "explanation": "The Aburame clan cultivates kikaichu insects that live in their bodies.", "category": "Clans & Dojutsu"},
    {"question": "Which clan does Shikamaru belong to?", "options": ["Nara", "Akimichi", "Yamanaka", "Aburame"], "answer": "Nara", "explanation": "The Nara clan is known for shadow techniques and exceptional strategic skill.", "category": "Clans & Dojutsu"},
    {"question": "What visual feature defines a standard active Byakugan eye?", "options": ["Bulging veins around temples", "Red colored irises", "Rippled circular patterns", "Spinning black tomoe"], "answer": "Bulging veins around temples", "explanation": "Activating the Byakugan causes the veins around the user's eyes to protrude severely.", "category": "Clans & Dojutsu"},
    {"question": "What is the highest evolutionary stage of the Sharingan eye?", "options": ["Rinnegan", "Mangekyō Sharingan", "Byakugan", "Tenseigan"], "answer": "Mangekyō Sharingan", "explanation": "The Mangekyō Sharingan is an advanced mutation triggered by emotional trauma.", "category": "Clans & Dojutsu"},
    {"question": "What design pattern characterizes the absolute base Sharingan?", "options": ["Tomoe seals", "Ripples", "A cross symbol", "A white blank void"], "answer": "Tomoe seals", "explanation": "The base Sharingan features up to three black pinwheel marks called tomoe.", "category": "Clans & Dojutsu"},
    {"question": "Which eye technique features concentric rippled circles across a purple iris?", "options": ["Rinnegan", "Sharingan", "Ketsuryugan", "Byakugan"], "answer": "Rinnegan", "explanation": "The Rinnegan appears as a ripple pattern extending over the eyeball.", "category": "Clans & Dojutsu"},
    {"question": "How does an Uchiha typically unlock the base Sharingan?", "options": ["Experiencing intense emotion", "Rigorous physical lifting", "Eating special herbs", "Meditating under water"], "answer": "Experiencing intense emotion", "explanation": "Strong trauma or protective love releases special chakra into the optic nerve.", "category": "Clans & Dojutsu"},
    {"question": "What blinding consequence comes from overusing the Mangekyō Sharingan?", "options": ["Permanent blindness", "Chakra depletion", "Memory loss", "Deafness"], "answer": "Permanent blindness", "explanation": "Frequent use of the Mangekyō gradually degrades the user's eyesight until they go blind.", "category": "Clans & Dojutsu"},
    {"question": "How can a shinobi stop the blindness caused by the Mangekyō Sharingan?", "options": ["Transplanting a sibling's eyes", "Learning Sage Mode", "Using medical high-level seals", "Bathing in hot springs"], "answer": "Transplanting a sibling's eyes", "explanation": "Transplanting the Mangekyō eyes of a close relative awakens the Eternal Mangekyō Sharingan.", "category": "Clans & Dojutsu"},
    {"question": "Which Uchiha first unlocked the Eternal Mangekyō Sharingan?", "options": ["Madara Uchiha", "Itachi Uchiha", "Sasuke Uchiha", "Obito Uchiha"], "answer": "Madara Uchiha", "explanation": "Madara took the eyes of his brother Izuna to gain permanent light.", "category": "Clans & Dojutsu"},
    {"question": "Which clan possesses the signature ability to expand their body size and mass?", "options": ["Akimichi Clan", "Nara Clan", "Yamanaka Clan", "Inuzuka Clan"], "answer": "Akimichi Clan", "explanation": "The Akimichi use Yang Release to convert calories into giant size expansion.", "category": "Clans & Dojutsu"},
    {"question": "Which clan is globally famous for Mind Transfer jutsu and flower arrangement?", "options": ["Yamanaka Clan", "Nara Clan", "Aburame Clan", "Kurama Clan"], "answer": "Yamanaka Clan", "explanation": "The Yamanaka specialize in spiritual body displacement and telepathic networks.", "category": "Clans & Dojutsu"},
    {"question": "What animal companion always fights alongside members of the Inuzuka Clan?", "options": ["Ninken (Dogs)", "Crows", "Toads", "Snakes"], "answer": "Ninken (Dogs)", "explanation": "Inuzuka clan members are partnered with ninja dogs (ninken) from infancy.", "category": "Clans & Dojutsu"},
    {"question": "What color is the hair of almost all pure-blooded Uzumaki clan members?", "options": ["Red", "Blonde", "Black", "Silver"], "answer": "Red", "explanation": "Vibrant red hair is the trademark trait of the Uzumaki lineage.", "category": "Clans & Dojutsu"},
    {"question": "Why did the Senju Clan fade out as an individual insular family group?", "options": ["Intermarried into the village", "Killed in the first war", "Left the country entirely", "Executed by Hokage orders"], "answer": "Intermarried into the village", "explanation": "The Senju deliberately integrated completely into Konoha to unify the populace.", "category": "Clans & Dojutsu"},
    {"question": "Which clan has a strict inner family division between Main and Branch houses?", "options": ["Hyuga Clan", "Uchiha Clan", "Kaguya Clan", "Hozuki Clan"], "answer": "Hyuga Clan", "explanation": "The Hyuga systematically oppress the Branch house to keep the Byakugan secure.", "category": "Clans & Dojutsu"},
    {"question": "What is the purpose of the curse mark placed on Hyuga Branch family members?", "options": ["Seals the eye upon death", "Increases physical strength", "Allows remote telepathy", "Blocks all genjutsu"], "answer": "Seals the eye upon death", "explanation": "The Caged Bird Seal destroys the Byakugan upon death to stop enemies from stealing it.", "category": "Clans & Dojutsu"},
    {"question": "Which clan is known for turning their bodies into liquid or water components?", "options": ["Hozuki Clan", "Yuki Clan", "Chinoike Clan", "Kamizuru Clan"], "answer": "Hozuki Clan", "explanation": "Suigetsu and Mangetsu belong to the Hozuki clan, utilizing Hydrification Jutsu.", "category": "Clans & Dojutsu"},
    {"question": "Which clan possesses the Kekkei Genkai to manipulate bones at will?", "options": ["Kaguya Clan", "Iburi Clan", "Jugo's Clan", "Kurama Clan"], "answer": "Kaguya Clan", "explanation": "Kimimaro's Kaguya clan uses Shikotsumyaku to manipulate skeletal cells.", "category": "Clans & Dojutsu"},
    {"question": "Which dojutsu did Nagato possess throughout his lifetime?", "options": ["Rinnegan", "Sharingan", "Byakugan", "Ketsuryugan"], "answer": "Rinnegan", "explanation": "Nagato was secretly given Madara Uchiha's Rinnegan when he was a child.", "category": "Clans & Dojutsu"},
    {"question": "What unique physical trait allows Karin to heal injured people?", "options": ["Biting her skin", "Placing her hands on them", "Her specialized red tears", "Transfusing her blood"], "answer": "Biting her skin", "explanation": "Injured allies bite Karin's skin to absorb her dense heal-inducing Uzumaki chakra.", "category": "Clans & Dojutsu"},
    {"question": "Which clan can absorb natural energy directly without any sage training?", "options": ["Jugo's Clan", "Senju Clan", "Hatake Clan", "Sarutobi Clan"], "answer": "Jugo's Clan", "explanation": "Jugo's nameless clan automatically absorbs natural power, causing erratic rage fits.", "category": "Clans & Dojutsu"},

    # --- JUTSU & SAGE MODE (25 Questions) ---
    {"question": "Who taught Naruto the Rasengan?", "options": ["Kakashi", "Jiraiya", "Iruka", "Yamato"], "answer": "Jiraiya", "explanation": "Jiraiya taught Naruto the Rasengan, a technique created by Minato.", "category": "Jutsu"},
    {"question": "Who created the Chidori?", "options": ["Sasuke Uchiha", "Kakashi Hatake", "Itachi Uchiha", "Orochimaru"], "answer": "Kakashi Hatake", "explanation": "Kakashi invented the Chidori and later taught it to Sasuke.", "category": "Jutsu"},
    {"question": "Which jutsu does Naruto learn from the Scroll of Seals?", "options": ["Flying Raijin", "Multi Shadow Clone Jutsu", "Chidori", "Summoning Jutsu"], "answer": "Multi Shadow Clone Jutsu", "explanation": "Naruto learns the Multi Shadow Clone Jutsu from the forbidden Scroll of Seals.", "category": "Jutsu"},
    {"question": "What is Haku's kekkei genkai?", "options": ["Lava Release", "Ice Release", "Wood Release", "Boil Release"], "answer": "Ice Release", "explanation": "Haku combines Water and Wind Release to use Ice Release.", "category": "Jutsu"},
    {"question": "Where does Naruto train to become a sage?", "options": ["Mount Myoboku", "Ryuchi Cave", "Shikkotsu Forest", "Valley of the End"], "answer": "Mount Myoboku", "explanation": "Naruto learns Sage Mode at Mount Myoboku, home of the toads.", "category": "Jutsu"},
    {"question": "What is Naruto's primary chakra nature?", "options": ["Wind", "Fire", "Lightning", "Earth"], "answer": "Wind", "explanation": "Naruto's natural affinity is Wind Release, which he uses to develop the Rasenshuriken.", "category": "Jutsu"},
    {"question": "Which fighting style is used by the Hyuga clan?", "options": ["Gentle Fist", "Strong Fist", "Drunken Fist", "Lightning Fist"], "answer": "Gentle Fist", "explanation": "The Hyuga use Gentle Fist to strike an opponent's chakra pathway system.", "category": "Jutsu"},
    {"question": "What elemental combination produces Wood Release?", "options": ["Earth and Water", "Fire and Earth", "Water and Wind", "Lightning and Earth"], "answer": "Earth and Water", "explanation": "Hashirama Senju combines Earth and Water chakra to generate living Wood Release.", "category": "Jutsu"},
    {"question": "What is the name of Sasuke's ultimate black flame technique?", "options": ["Amaterasu", "Tsukuyomi", "Kotoamatsukami", "Kirin"], "answer": "Amaterasu", "explanation": "Amaterasu produces unquenchable black flames at the user's focal point.", "category": "Jutsu"},
    {"question": "Which technique allows the user to summon a giant spectral warrior armor?", "options": ["Susanoo", "Kirin", "Shinra Tensei", "Edo Tensei"], "answer": "Susanoo", "explanation": "Those who awaken both Mangekyō Sharingan eyes can manifest the massive Susanoo armor.", "category": "Jutsu"},
    {"question": "What is the name of the ultimate Genjutsu that controls targets without them knowing?", "options": ["Kotoamatsukami", "Tsukuyomi", "Izanami", "Izanagi"], "answer": "Kotoamatsukami", "explanation": "Shisui Uchiha's Kotoamatsukami subtly controls minds completely undetected.", "category": "Jutsu"},
    {"question": "Which forbidden Uchiha jutsu rewrites reality at the cost of losing an eye?", "options": ["Izanagi", "Izanami", "Tsukuyomi", "Amaterasu"], "answer": "Izanagi", "explanation": "Izanagi turns real injuries or deaths into illusions for a brief duration.", "category": "Jutsu"},
    {"question": "Which jutsu was designed to counter Izanagi by trapping the victim in an infinite loop?", "options": ["Izanami", "Kotoamatsukami", "Tsukuyomi", "Kamui"], "answer": "Izanami", "explanation": "Izanami loops physical sensations until the target accepts their true fate.", "category": "Jutsu"},
    {"question": "What is the name of Kakashi's dimensional spatial eye technique?", "options": ["Kamui", "Amaterasu", "Tsukuyomi", "Kirin"], "answer": "Kamui", "explanation": "Kamui teleports matter to and from a distinct pocket dimension.", "category": "Jutsu"},
    {"question": "Which gate must Might Guy open to unlock the ultimate Night Guy evening attack?", "options": ["Eighth Gate of Death", "Seventh Gate of Wonder", "Sixth Gate of View", "Fifth Gate of Limit"], "answer": "Eighth Gate of Death", "explanation": "Opening the Eighth Gate converts blood into crimson heat vapor, ensuring death after use.", "category": "Jutsu"},
    {"question": "Who created the space-time teleportation jutsu, Flying Raijin?", "options": ["Tobirama Senju", "Minato Namikaze", "Hashirama Senju", "Madara Uchiha"], "answer": "Tobirama Senju", "explanation": "Tobirama Senju invented the Flying Raijin, though Minato later refined it to master status.", "category": "Jutsu"},
    {"question": "What animal contract must a shinobi sign to access the Strength of a Hundred seal?", "options": ["Toads", "Slugs", "Snakes", "Hawks"], "answer": "Slugs", "explanation": "Tsunade and Sakura summon Katsuyu the slug, tapping into the Katsuyu Network to heal armies.", "category": "Jutsu"},
    {"question": "What unique Sage Mode master physical change happens to Naruto's eyes?", "options": ["Orange pigment and horizontal lines", "Red irises and spinning patterns", "Purple circles", "Blank white eyes"], "answer": "Orange pigment and horizontal lines", "explanation": "Naruto gets orange eyeshadow pigment and horizontal toad-like rectangular pupils.", "category": "Jutsu"},
    {"question": "What is the drawback of Jiraiya's incomplete Sage Mode transformation?", "options": ["Takes on toad features", "Can only use it for 1 minute", "Blinds his left eye", "Loses his speech"], "answer": "Takes on toad features", "explanation": "Because Jiraiya hadn't fully balanced the energy, his nose expands and hands morph into toad parts.", "category": "Jutsu"},
    {"question": "Which snake sage proctors the Sage Mode training inside Ryuchi Cave?", "options": ["White Snake Sage", "Great Toad Sage", "Katsuyu", "Manda"], "answer": "White Snake Sage", "explanation": "The ancient White Snake Sage injects targets with snake venom to check for Sage suitability.", "category": "Jutsu"},
    {"question": "Who is the only character able to use Particle Release (Dust Release)?", "options": ["Ohnoki", "Mu", "Both Ohnoki and Mu", "Gaara"], "answer": "Both Ohnoki and Mu", "explanation": "The Second Tsuchikage Mu invented Particle Release and passed it to the Third Tsuchikage Ohnoki.", "category": "Jutsu"},
    {"question": "What form does Particle Release take when activated by the user?", "options": ["A glowing geometric structure", "A ball of mud", "A jet stream of water", "A lightning bolt"], "answer": "A glowing geometric structure", "explanation": "Particle Release manifests as a luminous cube, cone, or cylinder that atomizes targets.", "category": "Jutsu"},
    {"question": "What is the maximum number of shadow clones Naruto can safely summon in chapter 1?", "options": ["1000", "5", "50", "12"], "answer": "1000", "explanation": "Naruto overcomes Mizuki by summoning a massive army of a thousand clones.", "category": "Jutsu"},
    {"question": "Which jutsu requires three people to perform and teleports objects over massive distances?", "options": ["Flying Raijin Guiding Thunder", "Heavenly Transfer Jutsu", "Summoning Jutsu", "Kamui"], "answer": "Heavenly Transfer Jutsu", "explanation": "The Hidden Cloud uses Heavenly Transfer, though it typically rips normal human bodies apart.", "category": "Jutsu"},
    {"question": "What type of jutsu classification includes physical weapon strikes and martial arts?", "options": ["Taijutsu", "Ninjutsu", "Genjutsu", "Fuinjutsu"], "answer": "Taijutsu", "explanation": "Taijutsu refers to hand-to-hand martial combat requiring no hand signs.", "category": "Jutsu"},

    # --- TAILED BEASTS & AKATSUKI (25 Questions) ---
    {"question": "Which tailed beast is sealed inside Naruto?", "options": ["Shukaku", "Kurama", "Gyuki", "Son Goku"], "answer": "Kurama", "explanation": "Kurama is the Nine-Tailed Fox sealed within Naruto.", "category": "Tailed Beasts"},
    {"question": "Which tailed beast was sealed inside Gaara?", "options": ["Kurama", "Shukaku", "Matatabi", "Saiken"], "answer": "Shukaku", "explanation": "Gaara was the jinchuriki of Shukaku, the One-Tailed beast.", "category": "Tailed Beasts"},
    {"question": "What was the Akatsuki's main objective?", "options": ["Protect the Five Kage", "Collect the tailed beasts", "Restore the Uchiha clan", "Find the Sage of Six Paths"], "answer": "Collect the tailed beasts", "explanation": "Akatsuki captured the jinchuriki to gather all nine tailed beasts.", "category": "Akatsuki"},
    {"question": "What is Pain's true name?", "options": ["Yahiko", "Nagato", "Obito", "Kabuto"], "answer": "Nagato", "explanation": "Nagato uses the Six Paths of Pain to act as Akatsuki's apparent leader.", "category": "Akatsuki"},
    {"question": "Who defeats Asuma Sarutobi?", "options": ["Kakuzu", "Hidan", "Orochimaru", "Deidara"], "answer": "Hidan", "explanation": "Hidan kills Asuma with his ritual technique; Shikamaru later takes revenge.", "category": "Akatsuki"},
    {"question": "Who is the jinchuriki of the Eight-Tails?", "options": ["Killer B", "Yugito Nii", "Fuu", "Roshi"], "answer": "Killer B", "explanation": "Killer B is the Eight-Tails jinchuriki and the Raikage's adopted brother.", "category": "Tailed Beasts"},
    {"question": "What is the name of the Eight-Tails?", "options": ["Gyuki", "Isobu", "Kokuo", "Chomei"], "answer": "Gyuki", "explanation": "Gyuki is the Eight-Tails sealed inside Killer B.", "category": "Tailed Beasts"},
    {"question": "Which identity does Obito use while in Akatsuki?", "options": ["Tobi", "Zetsu", "Sasori", "Kakuzu"], "answer": "Tobi", "explanation": "Obito hides behind the playful Tobi persona for much of the series.", "category": "Akatsuki"},
    {"question": "Who is Itachi's Akatsuki partner?", "options": ["Kisame Hoshigaki", "Deidara", "Hidan", "Zetsu"], "answer": "Kisame Hoshigaki", "explanation": "Itachi and Kisame operate as an Akatsuki pair.", "category": "Akatsuki"},
    {"question": "What is the name of Kisame's living sword?", "options": ["Samehada", "Kubikiribocho", "Kiba", "Nuibari"], "answer": "Samehada", "explanation": "Samehada devours chakra and is Kisame's signature weapon.", "category": "Akatsuki"},
    {"question": "What does Deidara use to create his explosive art?", "options": ["Explosive clay", "Paper bombs", "Puppet cores", "Ink beasts"], "answer": "Explosive clay", "explanation": "Deidara molds explosive clay with the mouths in his hands.", "category": "Akatsuki"},
    {"question": "What material forms Konan's signature jutsu?", "options": ["Paper", "Sand", "Mist", "Wood"], "answer": "Paper", "explanation": "Konan can turn her body into paper and use it for offense and defense.", "category": "Akatsuki"},
    {"question": "How many total hearts does Kakuzu possess simultaneously?", "options": ["5", "4", "1", "9"], "answer": "5", "explanation": "Kakuzu harvests the organs of his victims, maintaining 5 elemental hearts.", "category": "Akatsuki"},
    {"question": "Which religious entity does Hidan worship to get his immortality?", "options": ["Jashin", "Hagoromo", "Kaguya", "Shinigami"], "answer": "Jashin", "explanation": "Hidan follows the radical cult of Lord Jashin, which demands bloodshed.", "category": "Akatsuki"},
    {"question": "What is Sasori's preferred weapon mechanism?", "options": ["Puppets", "Swords", "Explosives", "Poison gas clouds"], "answer": "Puppets", "explanation": "Sasori is a master puppeteer who turned his own body into a puppet core.", "category": "Akatsuki"},
    {"question": "Which historical Kage puppet did Sasori use as his personal favorite tool?", "options": ["Third Kazekage", "Second Mizukage", "First Hokage", "Fourth Kazekage"], "answer": "Third Kazekage", "explanation": "Sasori murdered the Third Kazekage to convert him into a weapon with Iron Sand.", "category": "Akatsuki"},
    {"question": "What is the name of the giant shell entity Akatsuki uses to store captured beasts?", "options": ["Gedo Mazo", "Katsuyu", "Shinigami Statue", "The Toad Tablet"], "answer": "Gedo Mazo", "explanation": "The Gedo Mazo (Demonic Statue of the Outer Path) serves as the husk of the Ten-Tails.", "category": "Akatsuki"},
    {"question": "Who was the jinchuriki of the Two-Tails, Matatabi?", "options": ["Yugito Nii", "Roshi", "Han", "Utakata"], "answer": "Yugito Nii", "explanation": "Yugito Nii was a proud kunoichi from the Cloud who mastered her blue fire beast.", "category": "Tailed Beasts"},
    {"question": "Which tailed beast takes the structural form of a giant blue fire cat?", "options": ["Matatabi", "Isobu", "Kokuo", "Saiken"], "answer": "Matatabi", "explanation": "Matatabi is the Two-Tails, looking like a massive flaming feline.", "category": "Tailed Beasts"},
    {"question": "What animal structure represents the Three-Tails, Isobu?", "options": ["A giant turtle", "A monkey", "A slug", "A horse-beetle hybrid"], "answer": "A giant turtle", "explanation": "Isobu is the Three-Tails, which resembles a heavily armored sea turtle.", "category": "Tailed Beasts"},
    {"question": "Which hidden village did the Six-Tails jinchuriki, Utakata, desert?", "options": ["Hidden Mist", "Hidden Stone", "Hidden Cloud", "Hidden Sand"], "answer": "Hidden Mist", "explanation": "Utakata was a rogue bubble-blowing shinobi who fled the Hidden Mist.", "category": "Tailed Beasts"},
    {"question": "What color are the signature cloaks worn by all Akatsuki members?", "options": ["Black with red clouds", "Purple with white streaks", "Pure crimson red", "Deep dark navy blue"], "answer": "Black with red clouds", "explanation": "The black cloaks decorated with red clouds symbolize the rain of blood that fell on Amegakure.", "category": "Akatsuki"},
    {"question": "Which Akatsuki member acted as a double-agent spy for the hidden Leaf?", "options": ["Itachi Uchiha", "Kisame Hoshigaki", "Sasori", "Deidara"], "answer": "Itachi Uchiha", "explanation": "Itachi joined Akatsuki to keep an eye on the organization and protect Konoha from afar.", "category": "Akatsuki"},
    {"question": "What physical body modification allowed Pain to remotely control his vessels?", "options": ["Black receiver piercings", "Chakra threads", "Tattoos", "Curse mark seals"], "answer": "Black receiver piercings", "explanation": "Nagato transmits his chakra through black metal rods placed in the bodies of the Paths.", "category": "Akatsuki"},
    {"question": "Who was Sasori's first partner in the Akatsuki before Deidara joined?", "options": ["Orochimaru", "Itachi", "Kakuzu", "Hidan"], "answer": "Orochimaru", "explanation": "Orochimaru worked with Sasori before abandoning the organization.", "category": "Akatsuki"},

    # --- GREAT WAR & LATE GAME (20 Questions) ---
    {"question": "Which forbidden technique restores the dead to temporary life?", "options": ["Edo Tensei", "Izanagi", "Reaper Death Seal", "Cursed Seal"], "answer": "Edo Tensei", "explanation": "Edo Tensei, or Reanimation Jutsu, summons the souls of the deceased into living vessels.", "category": "Fourth Great Ninja War"},
    {"question": "Who originally created Edo Tensei?", "options": ["Tobirama Senju", "Orochimaru", "Kabuto Yakushi", "Hiruzen Sarutobi"], "answer": "Tobirama Senju", "explanation": "The Second Hokage, Tobirama Senju, created the Reanimation Jutsu.", "category": "Fourth Great Ninja War"},
    {"question": "Who uses Edo Tensei on a huge scale during the Fourth Great Ninja War?", "options": ["Kabuto Yakushi", "Kisame", "Danzo", "Sasori"], "answer": "Kabuto Yakushi", "explanation": "Kabuto allies with Obito and deploys a vast Edo Tensei army in the war.", "category": "Fourth Great Ninja War"},
    {"question": "Who do Naruto and Sasuke seal at the end of the Fourth Great Ninja War?", "options": ["Kaguya Otsutsuki", "Madara Uchiha", "Black Zetsu", "Hagoromo Otsutsuki"], "answer": "Kaguya Otsutsuki", "explanation": "Naruto and Sasuke use the Six Paths Chibaku Tensei to seal Kaguya.", "category": "Fourth Great Ninja War"},
    {"question": "What is the name of the massive flower tree structure used to drain humanity's chakra?", "options": ["The God Tree", "The Chakra Willow", "The Ten-Tails Bulb", "The Shinju Sprout"], "answer": "The God Tree", "explanation": "The God Tree absorbs the life force of those caught in the Infinite Tsukuyomi.", "category": "Fourth Great Ninja War"},
    {"question": "Which legendary rogue shinobi drops a massive meteor onto the Allied Shinobi Forces?", "options": ["Madara Uchiha", "Obito Uchiha", "Kabuto Yakushi", "Mu"], "answer": "Madara Uchiha", "explanation": "Madara shows his power by dropping two consecutive meteors using the Shattered Heaven jutsu.", "category": "Fourth Great Ninja War"},
    {"question": "Who becomes the first Jinchuriki of the Ten-Tails during the war?", "options": ["Obito Uchiha", "Madara Uchiha", "Naruto Uzumaki", "Hagoromo Otsutsuki"], "answer": "Obito Uchiha", "explanation": "Obito seals the incomplete Ten-Tails into himself before Madara does.", "category": "Fourth Great Ninja War"},
    {"question": "What name is given to the unified military coalition formed by all five lands?", "options": ["Allied Shinobi Forces", "Five Nations Vanguard", "The Shinobi League", "United Ninja Front"], "answer": "Allied Shinobi Forces", "explanation": "The five major villages unite for the first time under Gaara's speech to form the Allied Shinobi Forces.", "category": "Fourth Great Ninja War"},
    {"question": "Who serves as the Supreme Commander of the Allied Shinobi Forces?", "options": ["A (Fourth Raikage)", "Gaara", "Tsunade", "Ohnoki"], "answer": "A (Fourth Raikage)", "explanation": "The Fourth Raikage A leads the overall war strategy, while Gaara manages field operations.", "category": "Fourth Great Ninja War"},
    {"question": "Which division of the army was led directly by Gaara?", "options": ["Fourth Division (Long-Range)", "First Division (Mid-Range)", "Second Division (Close-Range)", "Medical Division"], "answer": "Fourth Division (Long-Range)", "explanation": "Gaara commands the Fourth combat division along with acting as the Regimental Commander.", "category": "Fourth Great Ninja War"},
    {"question": "Who is the master strategist who commands operations from headquarters before it gets vaporized?", "options": ["Shikaku Nara", "Inoichi Yamanaka", "Ao", "Mabui"], "answer": "Shikaku Nara", "explanation": "Shikamaru's father, Shikaku Nara, plots out the army strategy from the Leaf headquarters.", "category": "Fourth Great Ninja War"},
    {"question": "Which beloved Team 7 peer dies protecting Naruto and Hinata from wood spikes?", "options": ["Neji Hyuga", "Rock Lee", "Choji Akimichi", "Kiba Inuzuka"], "answer": "Neji Hyuga", "explanation": "Neji acts as a human shield to save Naruto from the Ten-Tails' projectile attacks.", "category": "Fourth Great Ninja War"},
    {"question": "What items are used by Tenten to launch weapons during battles?", "options": ["Storage Scrolls", "Chakra strings", "Mechanical launchers", "Summoning gloves"], "answer": "Storage Scrolls", "explanation": "Tenten stores a vast armory of tools inside unrolled scrolls.", "category": "Fourth Great Ninja War"},
    {"question": "Which legendary tool of the Sage of Six Paths can seal anyone who says their most spoken word?", "options": ["Benihisa", "Kohaku no Johei", "Shichiseiuken", "Bashosen"], "answer": "Benihisa", "explanation": "The Crimson Gourd (Benihisa) records and sucks in victims who repeat their favorite phrase.", "category": "Fourth Great Ninja War"},
    {"question": "What powerful transformation gives Naruto spherical truth-seeking balls floating behind his back?", "options": ["Six Paths Sage Mode", "Nine-Tails Chakra Mode", "Tailed Beast Mode", "Toad Sage Mode"], "answer": "Six Paths Sage Mode", "explanation": "Hagoromo gives Naruto Six Paths powers, manifesting Truth-Seeking Orbs.", "category": "Fourth Great Ninja War"},
    {"question": "What physical feature does Sasuke gain in his left eye from the Sage of Six Paths?", "options": ["A six-tomoe Rinnegan", "An Eternal Sharingan", "A golden Byakugan", "A Tenseigan"], "answer": "A six-tomoe Rinnegan", "explanation": "Sasuke gets a unique Rinnegan containing six tomoe rings in his left eye.", "category": "Fourth Great Ninja War"},
    {"question": "Which character surprises Madara Uchiha by nearly beating him with pure Taijutsu blows?", "options": ["Might Guy", "Naruto Uzumaki", "Sasuke Uchiha", "Killer B"], "answer": "Might Guy", "explanation": "Madara declares Might Guy the strongest Taijutsu user after facing the Night Guy form.", "category": "Fourth Great Ninja War"},
    {"question": "What type of massive construct does the Allied Forces build out of earth walls to slow the Ten-Tails?", "options": ["Multi-layered Earth Rampart", "Mud Citadel", "Stone Dome", "Mountain Fortress"], "answer": "Multi-layered Earth Rampart", "explanation": "Shinobi synchronize their techniques to create dozens of concrete layers to stop a Tailed Beast Bomb.", "category": "Fourth Great Ninja War"},
    {"question": "Who finally puts an end to the Infinite Tsukuyomi illusion across the world?", "options": ["Naruto and Sasuke together", "Naruto alone", "Hagoromo Otsutsuki", "Kakashi Hatake"], "answer": "Naruto and Sasuke together", "explanation": "Forming the Rat hand sign together using their remaining hands undoes the absolute genjutsu.", "category": "Fourth Great Ninja War"},
    {"question": "What injury do Naruto and Sasuke both suffer during their final battle at the Valley of the End?", "options": ["Losing one arm", "Going permanently blind", "Losing their legs", "A cursed scar on their chest"], "answer": "Losing one arm", "explanation": "Their massive Chidori and Rasengan clash obliterates their dominant arms.", "category": "Fourth Great Ninja War"}

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
