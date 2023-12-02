@echo off
title "Checking software ..."

where python3 >nul 2>nul
if %errorlevel%==1 (
    @echo Python not found, please install Python 3 from https://python.org.
    pause
    exit 0
)

where java >nul 2>nul
if %errorlevel%==1 (
    @echo Java not found, please install Java 8 from https://java.com
    pause
    exit 0
)

python3 -m pip install -r requirements.txt

title "Running ..."

python3 autoeagler.py

echo Script exited.

timeout 5