#!/bin/sh
# usage: mix_audio.sh <brand_video_with_music.mp4>   (needs sfx.wav from sfx.py; 22 s total)
# Music: trimmed 0.36 s so its ~120 BPM grid lands on multiples of 0.5 s; first 16 s, then a beat-aligned
# (16-beat offset) repeat of its 8.36-14.5 s groove, crossfaded, to fill 22 s. Mixed to -14 LUFS.
ffmpeg -y -ss 0.36 -t 16.0 -i "$1" -vn -ar 44100 -ac 2 mA.wav
ffmpeg -y -ss 8.36 -t 6.15 -i "$1" -vn -ar 44100 -ac 2 mB.wav
ffmpeg -y -i mA.wav -i mB.wav -filter_complex "[0:a][1:a]acrossfade=d=0.15:c1=tri:c2=tri[a]" -map "[a]" music4.wav
ffmpeg -y -i music4.wav -i sfx.wav -filter_complex "[0:a]volume=0.85,afade=t=in:d=0.15,afade=t=out:st=20.2:d=1.8[m];[1:a]volume=1.0[s];[m][s]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]" -map "[a]" -ar 44100 -t 22 audio4.wav
