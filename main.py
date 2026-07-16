import os
import requests
import json


# načtení OpenRouter API klíče

api_key = os.getenv("OPENROUTER_API_KEY")


if not api_key:
    print("OpenRouter API klíč chybí ❌")
    exit()


print("OpenRouter API klíč nalezen ✅")


# prompt pro AI

prompt = """
Vytvoř 4 virální scénáře pro YouTube Shorts a TikTok.

Požadavky:
- délka videa 30 až 60 sekund
- silný hook během prvních 3 sekund
- témata: zajímavosti, historie, věda, záhady
- každý scénář musí mít:
  title
  hook
  script

Vrať pouze čistý JSON.
Nevkládej žádné ``` značky.
Nevysvětluj nic před ani za JSON.

Formát:

[
 {
  "title": "",
  "hook": "",
  "script": ""
 }
]
"""


print("Volám OpenRouter AI...")


# požadavek na OpenRouter

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
)


# kontrola odpovědi

if response.status_code != 200:
    print("Chyba OpenRouter:")
    print(response.text)
    exit()


data = response.json()


result = data["choices"][0]["message"]["content"]


print("AI odpověď:")
print(result)


# vyčištění odpovědi

result = result.replace("```json", "")
result = result.replace("```", "")

result = result.replace("\n", " ")
result = result.replace("\r", " ")
result = result.replace("\t", " ")

result = result.strip()


# najdeme pouze JSON část

start = result.find("[")
end = result.rfind("]") + 1


if start == -1 or end == 0:
    print("JSON nebyl nalezen ❌")
    exit()


result = result[start:end]


# kontrola JSON

try:
    scenarios = json.loads(result)

except Exception as e:
    print("JSON chyba ❌")
    print(e)
    print("Výsledek AI:")
    print(result)
    exit()


# uložení souboru

with open(
    "shorts_scenare.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        scenarios,
        file,
        ensure_ascii=False,
        indent=2
    )


print("Hotovo ✅ shorts_scenare.json vytvořen")
