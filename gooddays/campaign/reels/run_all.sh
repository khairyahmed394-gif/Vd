#!/bin/bash
# renders every reel in both languages (4 parallel jobs), then loudness-normalises (-14 LUFS)
cd "$(dirname "$0")"
for r in $(python3 -c "from cfg import REELS;print(' '.join(REELS))"); do for l in ar en; do echo "$r $l"; done; done | xargs -P4 -L1 bash -c 'python3 render.py $0 $1 full out/$1/raw_$0.mp4 audio/$0.wav'
for f in out/*/raw_*.mp4; do d=$(dirname $f); b=$(basename $f | sed 's/raw_//'); ffmpeg -loglevel error -y -i $f -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=7 -c:a aac -b:a 192k -movflags +faststart $d/$b && rm $f; done
