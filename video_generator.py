import json
import whisper

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


print(title)


# vytvoření hlasu

tts = gTTS(
    text=script,
    lang="cs"
)

tts.save(
    "voice.mp3"
)


print("Hlas vytvořen ✅")


# Whisper rozpoznání

print("Generuji titulky...")


model = whisper.load_model(
    "base"
)


result = model.transcribe(
    "voice.mp3",
    language="cs"
)


subtitle_text = result["text"]


print(
    subtitle_text
)


# obrázek

background = ImageClip(
    "images/pyramid.jpg"
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
    size=(1000, None),
    method="caption"
)

title_clip = title_clip.with_position(
    ("center","center")
)

title_clip = title_clip.with_duration(10)


# spodní titulky

subtitle = TextClip(
    text=subtitle_text,
    font_size=45,
    color="white",
    size=(1000,None),
    method="caption"
)

subtitle = subtitle.with_position(
    ("center","bottom")
)

subtitle = subtitle.with_duration(10)


# video

final = CompositeVideoClip(
    [
        background,
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
    "short_with_subtitles.mp4",
    fps=24
)


print("Hotovo ✅ short_with_subtitles.mp4")
