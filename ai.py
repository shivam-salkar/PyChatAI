# groq_client.py
from groq import Groq
import dotenv
import pyttsx3

dotenv.load_dotenv()
client = Groq()
engine = pyttsx3.init()
engine.setProperty('rate', 250)

def return_prompt(prompt):
    response = client.chat.completions.create(
        model="compound-beta",
        messages=[{"role": "user", "content": "" + prompt}],
        temperature=0.7,
        max_tokens=512,
        top_p=1,
    )
    return response.choices[0].message.content

def tts(text: str):
    if text.strip() == '':
        return
    
    engine.say(text)
    engine.runAndWait()