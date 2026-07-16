import json

from gtts import gTTS

from moviepy import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    AudioFileClip
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


video = scenarios[0]

title = video["title"]
script = video["script"]


print("Vytvářím video:")
print(title)


# vytvoření hlasu

print("Generuji AI hlas...")


tts = gTTS(
    text=script,
    lang="cs"
)

tts.save(
    "voice.mp3"
)


print("Hlas vytvořen ✅")


# obrázek

background = ImageClip(
    "images/pyramid.jpg"
)

background = background.resized(
    height=1920
)

background = background.with_duration(10)


# text

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

text = text.with_duration(10)


# spojení

video_clip = CompositeVideoClip(
    [
        background,
        text
    ],
    size=(1080,1920)
)


# přidání hlasu

audio = AudioFileClip(
    "voice.mp3"
)


video_clip = video_clip.with_audio(
    audio
)


# export

video_clip.write_videofile(
    "short_with_voice.mp4",
    fps=24
)


print("Hotovo ✅ short_with_voice.mp4")
