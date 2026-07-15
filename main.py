import os
from datetime import datetime
from google import genai


print("============================")
print("AI Shorts Robot spuštěn")
print(datetime.now())
print("============================")


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Chybí API klíč")
    exit()


client = genai.Client(
    api_key=api_key
)


response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="""
Vytvoř 4 virální YouTube Shorts scénáře.

Pro každý napiš:
- název
- hook první 3 sekundy
- scénář na 45 sekund
- návrh scén

Téma:
zajímavá fakta
"""
)


print("============================")
print(response.text)
print("============================")
