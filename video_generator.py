import json
import os
import requests
import whisper

from gtts import gTTS

from moviepy import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    AudioFileClip,
    concatenate_videoclips
)


print("Spouštím video generátor...")


os.makedirs("images", exist_ok=True)
os.makedirs("videos", exist_ok=True)



with open(
    "shorts_scenare.json",
    "r",
    encoding="utf-8"
) as file:
    data = json.load(file)


scenario = data[0]

title = scenario["title"]
scenes = scenario["scenes"]


print("Video:")
print(title)

print(
    "Počet scén:",
    len(scenes)
)



# hlas

text = " ".join(
    scene["text"]
    for scene in scenes
)


print("Vytvářím hlas...")


tts = gTTS(
    text=text,
    lang="cs"
)

tts.save(
    "voice.mp3"
)


print("Hlas hotový ✅")



# obrázky

images = []


print("Stahuji obrázky...")


for i, scene in enumerate(scenes):

    filename = f"images/scene_{i}.jpg"


    url = (
        f"https://picsum.photos/1080/1920?random={i}"
    )


    r = requests.get(
        url,
        timeout=30
    )


    if not r.content.startswith(b"\xff\xd8"):

        print(
            "Špatný obrázek:",
            filename
        )
        continue


    with open(
        filename,
        "wb"
    ) as img:

        img.write(
            r.content
        )


    images.append(
        filename
    )


print(
    "Obrázky:",
    len(images)
)



# video scény

clips = []


for image in images:

    clip = ImageClip(
        image
    )


    clip = clip.resized(
        height=1920
    )


    clip = clip.with_duration(
        6
    )


    clips.append(
        clip
    )



video = concatenate_videoclips(
    clips
)



# titul

title_clip = TextClip(
    text=title.upper(),
    font_size=75,
    color="white",
    size=(1000,None),
    method="caption"
)


title_clip = title_clip.with_duration(
    video.duration
)


title_clip = title_clip.with_position(
    ("center","top")
)



final = CompositeVideoClip(
    [
        video,
        title_clip
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
    "videos/viral_short.mp4",
    fps=24
)


print("HOTOVO ✅")
