import json
from moviepy import (
    ImageClip,
    TextClip,
    CompositeVideoClip
)


print("Spouštím video generátor...")


# načtení scénářů

with open(
    "shorts_scenare.json",
    "r",
    encoding="utf-8"
) as file:
    scenarios = json.load(file)


print(f"Nalezeno scénářů: {len(scenarios)}")


# první scénář

video = scenarios[0]

title = video["title"]


print("Vytvářím video:")
print(title)


# obrázek pozadí

background = ImageClip(
    "images/pyramid.jpg"
)


background = background.resized(
    height=1920
)


background = background.with_duration(5)


# text přes obrázek

text = TextClip(
    text=title,
    font_size=80,
    color="white",
    size=(1000, None),
    method="caption"
)


text = text.with_position(
    ("center", "center")
)

text = text.with_duration(5)


# spojení

final_video = CompositeVideoClip(
    [
        background,
        text
    ],
    size=(1080,1920)
)


final_video.write_videofile(
    "short_image_test.mp4",
    fps=24
)


print("Hotovo ✅ short_image_test.mp4")
