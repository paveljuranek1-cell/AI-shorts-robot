import json
import os
import requests
import whisper

from duckduckgo_search import DDGS
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


video = scenarios[0]

title = video["title"]
script = video["script"]


print("Téma:")
print(title)


# vytvoření složky

os.makedirs(
    "images",
    exist_ok=True
)


# hledání obrázku

print("Hledám obrázek...")


query = title + " historical"


image_url = None


with DDGS() as ddgs:

    results = ddgs.images(
        query,
        max_results=1
    )

    for image in results:
        image_url = image["thumbnail"]
        break


if image_url:

    print("Obrázek nalezen ✅")


    img = requests.get(
        image_url
    ).content


    with open(
        "images/topic.jpg",
        "wb"
    ) as f:
        f.write(img)


else:

    print("Obrázek nenalezen ❌")
    exit()



# hlas

print("Generuji hlas...")


tts = gTTS(
    text=script,
    lang="cs"
)

tts.save(
    "voice.mp3"
)


print("Hlas vytvořen ✅")



# Whisper

model = whisper.load_model(
    "base"
)


result = model.transcribe(
    "voice.mp3",
    language="cs",
    word_timestamps=True
)



# pozadí

background = ImageClip(
    "images/topic.jpg"
)


background = background.resized(
    height=1920
)


background = background.with_duration(10)



# titulek

title_clip = TextClip(
    text=title,
    font_size=80,
    color="white",
    size=(1000,None),
    method="caption"
)


title_clip = title_clip.with_position(
    ("center","top")
)


title_clip = title_clip.with_duration(
    10
)



# titulky

subtitle_clips = []


for segment in result["segments"]:

    subtitle = TextClip(
        text=segment["text"].upper(),
        font_size=60,
        color="white",
        size=(1000,None),
        method="caption"
    )

    subtitle = subtitle.with_position(
        ("center","center")
    )

    subtitle = subtitle.with_start(
        segment["start"]
    )

    subtitle = subtitle.with_duration(
        segment["end"] - segment["start"]
    )

    subtitle_clips.append(
        subtitle
    )



final = CompositeVideoClip(
    [
        background,
        title_clip,
        *subtitle_clips
    ],
    size=(1080,1920)
)


audio = AudioFileClip(
    "voice.mp3"
)


final = final.with_audio(
    audio
)



final.write_videofile(
    "videos/auto_image_short.mp4",
    fps=24
)


print(
    "Hotovo ✅ videos/auto_image_short.mp4"
)
