import os
import requests
import json


# načtení OpenRouter API klíče z GitHub Secrets
api_key = os.getenv("OPENROUTER_API_KEY")


if not api_key:
    print("OpenRouter API klíč chybí ❌")
    exit()


print("OpenRouter API klíč nalezen ✅")


# požadavek pro AI
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

Vrať pouze JSON ve formátu:

[
 {
  "title": "",
  "hook": "",
  "script": ""
 }
]
"""


print("Volám OpenRouter AI...")


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


# kontrola chyby

if response.status_code != 200:
    print("Chyba OpenRouter:")
    print(response.text)
    exit()


data = response.json()


result = data["choices"][0]["message"]["content"]


print("AI odpověď:")
print(result)

# odstranění Markdown značek pokud je AI přidala

result = result.replace("```json", "")
result = result.replace("```", "")
result = result.strip()


# kontrola, že JSON opravdu funguje

scenarios = json.loads(result)


# uložení hezkého JSON souboru

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
