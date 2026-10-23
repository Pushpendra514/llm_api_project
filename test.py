import os
import dotenv
import requests
import datetime as dt
total = 25
subject = "aptitude"
topic = "profit and loss"
date = dt.datetime.now().date()
dotenv.load_dotenv()

# Prompt and stucture of output
aptitude_topics = [
    "Number System",
    "Percentage",
    "Ratio and Proportion",
    "Average",
    "Profit and Loss",
    "Simple Interest",
    "Compound Interest",
    "Time and Work",
    "Pipes and Cisterns",
    "Time, Speed and Distance",
    "Boats and Streams",
    "Problems on Trains",
    "Problems on Ages",
    "Partnership",
    "Mixture and Alligation",
    "HCF and LCM",
    "Permutation and Combination",
    "Probability",
    "Number Series",
    "Coding and Decoding",
    "Blood Relations",
    "Direction Sense",
    "Seating Arrangement",
    "Logical Reasoning",
    "Syllogism",
    "Data Interpretation",
    "Data Sufficiency",
    "Calendar",
    "Clock",
    "Algebra",
    "Geometry",
    "Mensuration",
    "Reading Comprehension",
    "Sentence Correction",
    "Synonyms and Antonyms",
    "Error Spotting"
]
try:
  with open("topic_counter.txt","r+") as fin:
    global topic_counter
    topic_counter = int(fin.read())
except FileNotFoundError:
  with open("topic_counter.txt","w", encoding="utf-8") as fin:
    fin.write("0")
    
    
    topic_counter = 0
    
prompt = (f"""
          Write {total} multiple-choice {subject} questions on "{aptitude_topics[topic_counter]}" for a practice set dated {date}. 
Aim for a campus-placement level. Each question must be self-contained, have exactly 4 options with one correct answer, 
and differ clearly from the others. Show the working briefly in the explanation. 
If the topic is "Mixed", spread the questions across the {subject} topics evenly.

Reply with only JSON in this exact shape and key names:

{{
  "type": "Daily",
  "subject": "{subject}",
  "date": "{date}",
  "topic": "{aptitude_topics[topic_counter]}",
  "total": {total},
  "questions": [
    {{
      "qno": 1,
      "question": "",
      "options": ["", "", "", ""],
      "solution" : {{
        "correct_option": 1,
        "correct_answer": "",
        "explanation": ""
      }}
    }}
  ]
}}

"qno" counts up from 1. "correct_option" is the position (1 to 4) of the right option, and "correct_answer" repeats that option's text exactly.
          """)

API_KEY = os.environ.get("API_KEY")

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "openrouter/free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
)

if not response.ok:
    print(response.status_code, response.text)
    print(response.headers.get("X-RateLimit-Reset"))
response.raise_for_status()
response.raise_for_status()
data = response.json()
with open("question.json","w",encoding="utf-8") as fin:
    fin.write(data["choices"][0]["message"]["content"])

print(data["choices"][0]["message"]["content"])
print("Model used:", data["model"])
with open("topic_counter.txt","w",encoding="utf-8") as fin:
  topic_counter = topic_counter + 1
  fin.write(str(topic_counter))