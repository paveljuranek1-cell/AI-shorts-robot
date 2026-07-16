import os
import json
import requests


print("Spouštím AI Shorts generátor...")


api_key = os.getenv(
    "OPENROUTER_API_KEY"
)


if not api_key:
    print("OPENROUTER_API_KEY chybí")
    exit()



prompt = """
Jsi profesionální tvůrce virálních YouTube Shorts.

Vytvoř jeden scénář pro video 40 sekund.

Vyber téma:
- záhady
- vesmír
- historie
- věda
- zvířata
- nevysvětlitelné objevy
- technologie

Pravidla:
- první věta musí být extrémně zajímavá
- každá scéna musí držet pozornost
- text musí být vhodný pro český AI hlas
- každá scéna 6-8 sekund

Vrať POUZE JSON:

{
"title":"virální název",
"hook":"první šokující věta",
"scenes":[
{
"text":"mluvený text scény",
"image":"detailní popis obrázku"
},
{
"text":"mluvený text scény",
"image":"detailní popis obrázku"
},
{
"text":"mluvený text scény",
"image":"detailní popis obrázku"
},
{
"text":"mluvený text scény",
"image":"detailní popis obrázku"
},
{
"text":"mluvený text scény",
"image":"detailní popis obrázku"
}
]
}
"""


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
                "role":"user",
                "content":prompt
            }
        ]
    },
    timeout=60
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


scenario = json.loads(
    content
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



print("================================")
print("SCÉNÁŘ HOTOVÝ ✅")
print(
    scenario["title"]
)

print(
    "Scén:",
    len(scenario["scenes"])
)

print("================================")
