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
    AudioFileClip,
    concatenate_videoclips
)


print("Spouštím video generátor...")


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


scenario = data[0]


title = scenario["title"]

scenes = scenario["scenes"]


print("Video:")
print(title)

print(
    "Počet scén:",
    len(scenes)
)



# spojení textu pro hlas

full_text = " ".join(
    scene["text"]
    for scene in scenes
)


# vytvoření hlasu

print("Vytvářím hlas...")


tts = gTTS(
    text=full_text,
    lang="cs"
)


tts.save(
    "voice.mp3"
)


print("Hlas hotový ✅")



# obrázky

image_files = []


print("Stahuji obrázky...")


for index, scene in enumerate(
    scenes
):

    query = urllib.parse.quote(
        scene["image"]
    )


    url = (
        "https://loremflickr.com/1080/1920/"
        + query
    )


    response = requests.get(
        url,
        timeout=30
    )


    filename = (
        f"images/scene_{index}.jpg"
    )


    with open(
        filename,
        "wb"
    ) as img:

        img.write(
            response.content
        )


    image_files.append(
        filename
    )


print("Obrázky hotové ✅")



# vytvoření scén videa

clips = []


for image in image_files:

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



# titulky

subtitle = TextClip(
    text=full_text.upper(),
    font_size=50,
    color="white",
    size=(1000,None),
    method="caption"
)


subtitle = subtitle.with_duration(
    video.duration
)


subtitle = subtitle.with_position(
    ("center","bottom")
)



final = CompositeVideoClip(
    [
        video,
        title_clip,
        subtitle
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
print("HOTOVO ✅")
print(
    "videos/viral_short.mp4"
)
