import os
import google.generativeai as genai
import json


# načtení API klíče z GitHub Secrets
api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    print("API klíč chybí ❌")
    exit()


print("API klíč nalezen ✅")


# připojení Gemini
genai.configure(api_key=api_key)


# vyber model
model = genai.GenerativeModel("gemini-2.0-flash")


# zadání pro AI
prompt = """
Vytvoř 4 virální nápady pro YouTube Shorts a TikTok.

Požadavky:
- délka videa 30 až 60 sekund
- musí být zajímavé během prvních 3 sekund
- cílové publikum celosvětově
- témata: zajímavosti, historie, věda, záhady

Vrať výsledek jako JSON.

Formát:

[
 {
  "title": "",
  "hook": "",
  "script": ""
 }
]

Nevkládej žádný text mimo JSON.
"""


print("Volám Gemini...")


response = model.generate_content(prompt)


text = response.text


print("Gemini odpověď:")
print(text)


# uložíme výsledek

with open("shorts_scenare.json", "w", encoding="utf-8") as file:
    file.write(text)


print("Hotovo ✅ Soubor shorts_scenare.json vytvořen")
