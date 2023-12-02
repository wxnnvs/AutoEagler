@echo off
title AutoEagler | Checking software ...

python3 -m pip install -r requirements.txt

title AutoEagler | Running ...

python3 autoeagler.py

echo Script exited.

timeout 5