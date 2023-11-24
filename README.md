# AutoEagler
A tool to automaticly set up a localhost eaglerXbungee, aiming to provide an alternative to singleplayer for Eaglercraft

## Progress:
✅ Write autoeagler.py (local + NGROK)

✅ Add different regions to decrease ping

✅ Customisation options (gamemode, seed, etc)

🟠 Fix Linux support

## Usage:

### Installation

1. Download and install the latest [Python](https://python.org) release
2. Install pyngrok using `pip3 install pyngrok`
3. Install [Java 8](https://java.com/download/)
4. Download [the latest release](github.com/wxnnvs/AutoEagler/releases/latest) to a dedicated folder
5. Run `python3 autoeagler.py` in a terminal or CMD
6. Open up option `1`
7. Let it run for a while, it might pop up some windows, you're done when the main menu is back
8. Done!

### Local server

1. Run `python3 autoeagler.py` in a terminal or CMD
2. Open up option `2`
3. Let it run for a minute, it might pop up some windows
4. Join on `ws://localhost:8081` using an offline download
5. Press `[Enter]` to return to the menu
6. Open up option `5` to shut it down and close the program

### Public server (ngrok)

1. Run `python3 autoeagler.py` in a terminal or CMD
2. Open up option `3`
3. Let it run for a minute, it might pop up some windows
4. Join on `wss://<subdomain>.ngrok.io` using any client (link will be showed)
5. Press `[Enter]` to return to the menu
6. Open up option `5` to shut it down and close the program

# For Mojang:
This tool does **NOT** include any of the source code from Minecraft, MCP, or any other illegal/copyrighted resources, nor any info on how to get it.