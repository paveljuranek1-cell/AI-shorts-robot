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


with open(
    "shorts_scenare.json",
    "r",
    encoding="utf-8"
) as file:
    scenarios = json.load(file)


video = scenarios[0]

title = video["title"]
script = " ".join(
    scene["text"]
    for scene in video["scenes"]
)

print("Téma:")
print(title)


os.makedirs(
    "images",
    exist_ok=True
)


# obrázek

print("Stahuji obrázek...")


query = urllib.parse.quote(
    title
)


image_url = (
    "https://loremflickr.com/1080/1920/"
    + query
)


response = requests.get(
    image_url,
    timeout=30,
    allow_redirects=True
)


if response.headers.get("content-type","").startswith("image"):

    with open(
        "images/topic.jpg",
        "wb"
    ) as file:
        file.write(
            response.content
        )

    print("Obrázek připraven ✅")

else:

    print("Obrázek se nepodařilo stáhnout")
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



# whisper

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


background = background.with_duration(
    10
)



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
