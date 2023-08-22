from pytube import YouTube
import ffmpeg
import os

song_list = []
with open("songs.txt", "r") as f:
    for line in f.readlines():
        song_list.append({"url": line.split(" ")[0], "start": line.split(" ")[1]})

for song in song_list:
    yt = YouTube(song["url"])

    path = yt.streams.get_audio_only().download()
    input = ffmpeg.input(path)
    audio_cut = input.audio.filter("atrim", start=int(song["start"]), duration=25)
    faded = audio_cut.filter_("afade", t="in", st=song["start"], d="1").filter_(
        "afade", t="out", st=f"{int(song['start']) + 24}", d="1"
    )
    output = faded.output(f"./clips/{yt.title}.mp3").run()
    os.remove(path)
