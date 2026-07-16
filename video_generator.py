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


print("================================")
print("Spouštím video generátor")
print("================================")


os.makedirs(
    "images",
    exist_ok=True
)

os.makedirs(
    "videos",
    exist_ok=True
)



# načtení scénáře

with open(
    "shorts_scenare.json",
    "r",
    encoding="utf-8"
) as file:
    data = json.load(file)


video = data[0]


title = video["title"]

scenes = video["scenes"]


print(title)
print(
    "Scény:",
    len(scenes)
)



# vytvoření hlasu

full_text = " ".join(
    s["text"]
    for s in scenes
)


print("Tvořím hlas...")


tts = gTTS(
    full_text,
    lang="cs"
)


tts.save(
    "voice.mp3"
)


print("Hlas hotový ✅")



# obrázky

print("Stahuji obrázky...")


images = []


for i, scene in enumerate(scenes):

    url = (
        "https://picsum.photos/1080/1920?random="
        + str(i)
    )


    r = requests.get(
        url,
        timeout=30
    )


    filename = (
        f"images/scene{i}.jpg"
    )


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


print("Obrázky hotové ✅")



# video scény

clips = []


for img in images:

    clip = ImageClip(
        img
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



video_clip = concatenate_videoclips(
    clips
)



# hlavní titulek

title_clip = TextClip(
    text=title.upper(),
    font_size=80,
    color="white",
    size=(1000,None),
    method="caption"
)


title_clip = title_clip.with_duration(
    video_clip.duration
)


title_clip = title_clip.with_position(
    ("center","top")
)



final = CompositeVideoClip(
    [
        video_clip,
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



print()
print("==============================")
print("VIDEO HOTOVÉ ✅")
print("videos/viral_short.mp4")
print("==============================")
