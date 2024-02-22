# AutoEagler
A tool to automatically set up a localhost eaglerXbungee, aiming to provide an alternative to Eaglercraft's singleplayer

## Progress:
✅ Local + NGROK tunneling

✅ NGROK customisation

✅ Server customisation (gamemode, seed, etc)

✅ Multiple versions (1.3_beta + 1.5.2 + 1.8.8)

🟠 Docker deploy

### Installation (manual)

1. Download and install the latest [Python](https://python.org) release
3. Install [Java 8](https://java.com/download/)
4. Download [the latest release](https://github.com/wxnnvs/AutoEagler/releases/latest) to a dedicated folder
4. Unzip the zip file
5. Run `start.bat` in CMD
6. Open up option `1`
7. Let it run for a while, it might pop up some windows, you're done when the main menu is back
8. Done!

### Installation (docker)

1. Install [docker](https://www.docker.com/get-started/)
2. Run this command
```
docker run wxnnvs/autoeagler
```
3. Add a new server on your Eaglercraft client
4. Put in the given address (wss://<randomnumbers>.ngrok.io)

## Usage:

### Local server

1. Run `python3 autoeagler.py` or `start.bat` in  CMD
2. Open up option `2`
3. Let it run for a minute, it might pop up some windows
4. Join on `ws://localhost:8081` using an offline download
5. Press `[Enter]` to return to the menu
6. Open up option `5` to shut it down and close the program

### Public server (ngrok)

1. Run `python3 autoeagler.py` or `start.bat` in  CMD
2. Open up option `3`
3. Let it run for a minute, it might pop up some windows
4. Join on `wss://<subdomain>.ngrok.io` using any client (link will be showed)
5. Press `[Enter]` to return to the menu
6. Open up option `5` to shut it down and close the program

# For Mojang:
This tool does **NOT** include any of the source code from Minecraft, MCP, or any other illegal/copyrighted resources, nor any info on how to get it.