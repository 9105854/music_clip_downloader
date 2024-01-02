from pytube import YouTube
import ffmpeg
import os
from zipfile import ZipFile
import shutil
import sqlite3
def download_songs(file_path, file_name, job_id):
    db_connection = sqlite3.connect("jobs.db") 
    cursor = db_connection.cursor()
    cursor.execute(f"INSERT INTO jobs VALUES ('{str(job_id)}', 0, '')")
    db_connection.commit()
    song_list = []
    with open(file_path, "r") as f:
        for line in f.readlines():
            song_list.append({"url": line.split(" ")[0], "start": line.split(" ")[1]})
    file_titles = []
    fails = []

    folder = file_name.split('.')[0]

    clip_location = './clips/' + folder 
    while os.path.exists(clip_location):
        folder += '_new' 
        clip_location = './clips/' + folder 

    os.makedirs(clip_location)
    max = len(song_list) + 1
    number = 0
    progress = 0
    for song in song_list:
        try: 
            yt = YouTube(song["url"])

            path = yt.streams.get_audio_only().download()
            input = ffmpeg.input(path)
            audio_cut = input.audio.filter("atrim", start=int(song["start"]), duration=30)
            faded = audio_cut.filter_("afade", t="in", st=song["start"], d="1").filter_(
                "afade", t="out", st=f"{int(song['start']) + 29}", d="1"
            )
            title = yt.title
            title = title.replace(".", "").replace("/", "")
            if title in file_titles:
                title = f"{title} {file_titles.count(title) + 1}"
            file_titles.append(title)
            
            output = faded.output(f"{clip_location}/{title}.mp3").run()
            os.remove(path)
        except: 
            print(f"{song} Failed:")
            fails.append(song)
        number += 1
        progress = int((number / max) * 100)
        cursor.execute(f"UPDATE jobs SET progress = {progress} WHERE job_id = '{job_id}'")
        db_connection.commit()
    print("Finished")
    print(fails)
    with open("failed.txt", "w") as f:
        for line in fails:
            f.writelines(str(line))
    print('creating zip')
    with ZipFile(f'./static/{folder}.zip', 'w') as myzip:
        target_files = os.listdir(clip_location)
        for file in file_titles:
            path = f'{clip_location}/{file}.mp3'
            myzip.write(path, f"{file}.mp3")
    shutil.rmtree(clip_location)
    cursor.execute(f"UPDATE jobs SET progress = 100, final_file = '{folder}.zip' WHERE job_id = '{job_id}'")
    db_connection.commit()
    return f"{folder}.zip" 
            
