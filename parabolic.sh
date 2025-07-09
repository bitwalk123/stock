#!/bin/bash
cd "$(dirname ${0})" || exit
source venv/bin/activate

# parabolic SAR signal
python parabolic.py

git pull
git add parabolic/*/*/*/*.png
git add parabolic/*/*/*/*.xlsx
git commit -m "update"
git push
