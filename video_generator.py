import json
from moviepy import TextClip, CompositeVideoClip


print("Spouštím video generátor...")


# načtení scénářů

with open(
    "shorts_scenare.json",
    "r",
    encoding="utf-8"
) as file:
    scenarios = json.load(file)


print(f"Nalezeno scénářů: {len(scenarios)}")


# vyber první scénář

video = scenarios[0]


title = video["title"]
script = video["script"]


print("Vytvářím testovací video:")
print(title)


# vytvoření textu do videa

text = TextClip(
    text=title,
    font_size=70,
    color="white",
    size=(1080, 1920),
    method="caption"
)

text = text.with_duration(5)


# vytvoření videa

final_video = CompositeVideoClip(
    [text],
    size=(1080, 1920)
)


final_video.write_videofile(
    "short_test.mp4",
    fps=24
)


print("Video vytvořeno ✅ short_test.mp4")
