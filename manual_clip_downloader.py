from pytube import YouTube
import ffmpeg
import os

yt = YouTube("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

path = yt.streams.get_audio_only().download()
start = input("Enter start time in seconds: ")
input = ffmpeg.input(path)
audio_cut = input.audio.filter("atrim", start=int(start), duration=25)
faded = audio_cut.filter_("afade", t="in", st=start, d="1").filter_(
    "afade", t="out", st=f"{int(start) + 24}", d="1"
)
output = faded.output(f"./clips/{yt.title}.mp3").run()
os.remove(path)