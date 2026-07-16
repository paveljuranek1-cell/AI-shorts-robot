import os
import json
import requests


print("Spouštím AI Shorts generátor...")


API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)


if not API_KEY:
    print("Chybí OPENROUTER_API_KEY")
    exit()


prompt = """
Jsi expert na tvorbu virálních YouTube Shorts.

Vytvoř jeden krátký virální scénář v češtině.

Používej témata:
- záhady
- vesmír
- historie
- věda
- neuvěřitelné objevy
- tajemná místa
- zvířata

Pravidla:
- délka videa 35 až 45 sekund
- první věta musí okamžitě zaujmout
- styl jako populární Shorts kanály
- žádné vysvětlování mimo JSON

Vrať pouze JSON:

{
"title":"krátký silný název",
"hook":"první věta videa",
"scenes":[
 {
  "text":"mluvený text první scény",
  "image":"popis obrázku první scény"
 },
 {
  "text":"mluvený text druhé scény",
  "image":"popis obrázku druhé scény"
 },
 {
  "text":"mluvený text třetí scény",
  "image":"popis obrázku třetí scény"
 },
 {
  "text":"mluvený text čtvrté scény",
  "image":"popis obrázku čtvrté scény"
 },
 {
  "text":"mluvený text páté scény",
  "image":"popis obrázku páté scény"
 }
]
}
"""


response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
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
    },
    timeout=60
)


data = response.json()


text = data["choices"][0]["message"]["content"]


text = text.replace(
    "```json",
    ""
)

text = text.replace(
    "```",
    ""
)

text = text.strip()


scenario = json.loads(
    text
)


with open(
    "shorts_scenare.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        [scenario],
        file,
        ensure_ascii=False,
        indent=2
    )


print("Scénář vytvořen ✅")
print()
print("Název:")
print(
    scenario["title"]
)

print()
print(
    "Počet scén:",
    len(scenario["scenes"])
)
