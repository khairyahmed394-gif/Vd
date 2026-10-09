#!/bin/sh
# usage: mix_audio.sh <brand_video_with_music.mp4>   (needs sfx.wav from sfx.py)
# music is trimmed 0.36 s so its ~120 BPM beat grid lands on multiples of 0.5 s (all cuts sit on that grid)
ffmpeg -y -ss 0.36 -t 15 -i "$1" -vn -ar 44100 -ac 2 music3.wav
ffmpeg -y -i music3.wav -i sfx.wav -filter_complex "[0:a]volume=0.85,afade=t=in:d=0.15,afade=t=out:st=13.4:d=1.6[m];[1:a]volume=1.0[s];[m][s]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]" -map "[a]" -ar 44100 -t 15 audio3.wav
