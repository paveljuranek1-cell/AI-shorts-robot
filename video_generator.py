import os
import json
import requests
import urllib.parse
import asyncio

import edge_tts

from moviepy import (
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)


print("🎬 AI Shorts Video Generator 2.0")


os.makedirs("images", exist_ok=True)
os.makedirs("videos", exist_ok=True)


# načtení scénáře

with open(
    "shorts_scenare.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)


video = data[0]

title = video["title"]
scenes = video["scenes"]


print("Téma:")
print(title)


# ======================
# AI hlas
# ======================


text = " ".join(
    scene["text"]
    for scene in scenes
)


print("Generuji hlas...")


async def make_voice():

    communicate = edge_tts.Communicate(
        text,
        "cs-CZ-AntoninNeural"
    )

    await communicate.save(
        "voice.mp3"
    )


asyncio.run(
    make_voice()
)


print("Hlas hotový ✅")



# ======================
# obrázky
# ======================


images = []


print("Generuji obrázky...")


for i, scene in enumerate(scenes):

    prompt = urllib.parse.quote(
        scene["image_prompt"]
    )


    url = (
        "https://image.pollinations.ai/prompt/"
        + prompt
        + "?width=1080&height=1920"
    )


    response = requests.get(
        url,
        timeout=90
    )


    filename = (
        f"images/{i}.jpg"
    )


    with open(
        filename,
        "wb"
    ) as img:

        img.write(
            response.content
        )


    images.append(
        filename
    )


print("Obrázky hotové ✅")



# ======================
# video
# ======================


clips = []


for img in images:

    clip = ImageClip(
        img
    )


    clip = clip.resized(
        height=1920
    )


    clip = clip.with_duration(
        7
    )


    clips.append(
        clip
    )



background = concatenate_videoclips(
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
    background.duration
)


title_clip = title_clip.with_position(
    ("center","top")
)



final = CompositeVideoClip(
    [
        background,
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



print("===================")
print("VIDEO HOTOVÉ ✅")
print("===================")
