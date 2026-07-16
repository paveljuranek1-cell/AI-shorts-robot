import json
import os
import requests
import urllib.parse
import whisper

from gtts import gTTS

from moviepy import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    AudioFileClip
)


print("Spouštím video generátor...")


# scénáře

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


# složka obrázků

os.makedirs(
    "images",
    exist_ok=True
)


# stažení obrázku podle tématu

print("Stahuji obrázek...")


query = urllib.parse.quote(
    title
)


url = (
    "https://source.unsplash.com/1080x1920/?"
    + query
)


response = requests.get(
    url,
    timeout=20
)


with open(
    "images/topic.jpg",
    "wb"
) as file:
    file.write(
        response.content
    )


print("Obrázek připraven ✅")



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



# titulky

model = whisper.load_model(
    "base"
)


result = model.transcribe(
    "voice.mp3",
    language="cs",
    word_timestamps=True
)



# obrázek

background = ImageClip(
    "images/topic.jpg"
)


background = background.resized(
    height=1920
)


background = background.with_duration(
    10
)



# název

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

subs = []


for segment in result["segments"]:

    clip = TextClip(
        text=segment["text"].upper(),
        font_size=60,
        color="white",
        size=(1000,None),
        method="caption"
    )


    clip = clip.with_position(
        ("center","center")
    )


    clip = clip.with_start(
        segment["start"]
    )


    clip = clip.with_duration(
        segment["end"] - segment["start"]
    )


    subs.append(
        clip
    )



final = CompositeVideoClip(
    [
        background,
        title_clip,
        *subs
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
