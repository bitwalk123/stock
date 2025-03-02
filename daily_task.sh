#!/bin/bash
cd "$(dirname ${0})" || exit
source venv/bin/activate

# daily data update for trade
python up_down_ratio.py

git pull
git add report/*/*.html
git commit -m "update"
git push
