import os
import json
import requests


print("🤖 AI Shorts Robot 2.0")
print("Generuji virální scénář...")


api_key = os.getenv(
    "OPENROUTER_API_KEY"
)


if not api_key:
    print("Chybí OPENROUTER_API_KEY")
    exit()



prompt = """
Jsi nejlepší tvůrce YouTube Shorts.

Vytvoř jeden virální Shorts scénář v češtině.

Téma vyber podle toho, co má největší šanci na sledovanost:
- záhady
- šokující fakta
- historie
- vesmír
- věda
- zvířata
- technologie

Pravidla:
- délka 45 sekund
- první 3 sekundy musí zastavit scrollování
- každá scéna musí být vizuálně zajímavá
- text musí být přirozený pro český AI hlas

Vrať pouze JSON:

{
"title":"název videa",
"hook":"první věta",
"scenes":[
{
"text":"mluvený text",
"image_prompt":"detailní filmový popis obrázku"
},
{
"text":"mluvený text",
"image_prompt":"detailní filmový popis obrázku"
},
{
"text":"mluvený text",
"image_prompt":"detailní filmový popis obrázku"
},
{
"text":"mluvený text",
"image_prompt":"detailní filmový popis obrázku"
},
{
"text":"mluvený text",
"image_prompt":"detailní filmový popis obrázku"
},
{
"text":"mluvený text",
"image_prompt":"detailní filmový popis obrázku"
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
        "messages":[
            {
                "role":"user",
                "content":prompt
            }
        ]
    },
    timeout=60
)



result = response.json()


text = result["choices"][0]["message"]["content"]


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
) as f:

    json.dump(
        [scenario],
        f,
        ensure_ascii=False,
        indent=2
    )


print("========================")
print("SCÉNÁŘ HOTOVÝ ✅")
print(scenario["title"])
print(
    "Scén:",
    len(scenario["scenes"])
)
print("========================")
