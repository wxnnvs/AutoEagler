#!/bin/bash

echo "Checking software ..."

if ! command -v python3 > /dev/null 2>&1; then
    echo "Python not found, please install Python 3 from https://python.org."
    read -p "Press Enter to exit."
    exit 0
fi

if ! command -v java > /dev/null 2>&1; then
    echo "Java not found, please install Java 8 from https://java.com"
    read -p "Press Enter to exit."
    exit 0
fi

python3 -m pip install -r requirements.txt

echo "Running ..."

python3 autoeagler.py

echo "Script exited."

sleep 5
