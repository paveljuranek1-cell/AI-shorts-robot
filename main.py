import os
import google.generativeai as genai
from datetime import datetime


print("============================")
print("AI Shorts Robot spuštěn")
print(datetime.now())
print("============================")


# načtení API klíče
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Chybí GEMINI_API_KEY")
    exit()


genai.configure(
    api_key=api_key
)


model = genai.GenerativeModel(
    "gemini-2.0-flash"
)


prompt = """
Jsi expert na YouTube Shorts.

Vytvoř 4 virální krátká videa.

Pro každé napiš:

- Název
- Hook první 3 sekundy
- Scénář na 45 sekund
- Návrh scén

Téma:
zajímavá fakta
"""


response = model.generate_content(prompt)


print("============================")
print("GENEROVANÉ SCÉNÁŘE")
print("============================")

print(response.text)


print("============================")
print("Hotovo")
print("============================")
