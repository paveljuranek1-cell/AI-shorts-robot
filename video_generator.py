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


print(f"Nalezeno scénářů: {len(scenarios)}")


video = scenarios[0]

title = video["title"]
script = video["script"]


print("Téma:")
print(title)


# vytvoření hlasu

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

print("Analyzuji hlas pro titulky...")


model = whisper.load_model(
    "base"
)


result = model.transcribe(
    "voice.mp3",
    language="cs",
    word_timestamps=True
)


print("Titulky připraveny ✅")


# obrázek

background = ImageClip(
    "images/pyramid.jpg"
)


background = background.resized(
    height=1920
)


background = background.with_duration(10)


# hlavní titulek

title_clip = TextClip(
    text=title,
    font_size=80,
    color="white",
    size=(1000, None),
    method="caption"
)


title_clip = title_clip.with_position(
    ("center", "top")
)


title_clip = title_clip.with_duration(10)



# vytváření dynamických titulků

subtitle_clips = []


for segment in result["segments"]:

    text = segment["text"].strip()

    start = segment["start"]

    end = segment["end"]

    duration = end - start


    subtitle = TextClip(
        text=text.upper(),
        font_size=60,
        color="white",
        size=(1000, None),
        method="caption"
    )


    subtitle = subtitle.with_position(
        ("center", "center")
    )


    subtitle = subtitle.with_start(
        start
    )


    subtitle = subtitle.with_duration(
        duration
    )


    subtitle_clips.append(
        subtitle
    )



# spojení vrstev

clips = [
    background,
    title_clip
]


clips.extend(
    subtitle_clips
)



final = CompositeVideoClip(
    clips,
    size=(1080,1920)
)



# zvuk

audio = AudioFileClip(
    "voice.mp3"
)


final = final.with_audio(
    audio
)



# export

final.write_videofile(
    "videos/short_dynamic_subtitles.mp4",
    fps=24
)


print(
    "Hotovo ✅ videos/short_dynamic_subtitles.mp4"
)
