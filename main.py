import os
import json
import requests


print("Spouštím AI Shorts generátor...")


api_key = os.getenv(
    "OPENROUTER_API_KEY"
)


if not api_key:
    print("Chybí OPENROUTER API KEY")
    exit()


prompt = """
Vytvoř jeden virální YouTube Shorts scénář.

Téma musí být:
- záhada
- vesmír
- historie
- šokující fakt
- věda
- neuvěřitelný objev

Vrať pouze JSON.

Formát:

{
"title":"krátký virální název",
"hook":"první věta která zaujme",
"scenes":[
 {
  "text":"mluvený text scény",
  "image":"popis obrázku"
 },
 {
  "text":"mluvený text scény",
  "image":"popis obrázku"
 },
 {
  "text":"mluvený text scény",
  "image":"popis obrázku"
 }
]
}

Každá scéna 5-8 sekund.
"""


response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model":"openai/gpt-4o-mini",
        "messages":[
            {
                "role":"user",
                "content":prompt
            }
        ]
    }
)


data = response.json()


content = data["choices"][0]["message"]["content"]


content = content.replace(
    "```json",
    ""
)

content = content.replace(
    "```",
    ""
)

content = content.strip()


scenarios = json.loads(
    content
)


with open(
    "shorts_scenare.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        [scenarios],
        file,
        ensure_ascii=False,
        indent=2
    )


print("Scénář vytvořen ✅")
print(scenarios["title"])
