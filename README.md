# Welcome to Music Clip Downloader
## About
This is a simple python script that downloads youtube mp3s and trims them to be 25 seconds. 
It also fades in and out for 1 second. 
## Usage
Download the git repository using your method of choice. Simplest is to just download the zip file from the GitHub page. 
Then, populate the `song.txt` file in the format shown below. 
```https://www.youtube.com/watch?v=dQw4w9WgXcQ 120```
The first part is the youtube link, followed by a space, then the start time to cut **in seconds**. 
Each song needs to be on a new line. You can check the current `songs.txt` file for an example.
Then, run the program using python e.g.
```
python automatic_clip_downloader.py
```
You can also run the manual clip downloader, which will ask for the desired url and start time after the program is run, which needs to be entered in manually. 

## Requirements
To run this script, firstly you will have to have [python](https://www.python.org/) installed. 
You also need [pytube](https://pytube.io/en/latest/) and [ffmpeg-python](https://pypi.org/project/ffmpeg-python/), both can be installed using `pip`. 
For ffmpeg-python to work, you need to have [ffmeg](https://ffmpeg.org/) installed and added to PATH. 

## What is this for?
If you know, you know. 