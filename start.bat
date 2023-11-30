@echo off
title Server Main

echo Running script...

python -m pip install -r requirements.txt

python autoeagler.py

echo Script exited.

timeout 5