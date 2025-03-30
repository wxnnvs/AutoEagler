# [ARCHIVED]
Websites dissapeared making the installer useless.
Singleplayer is released on 1.8.8 making the idea useless. 
I officially declare this project as dead.
Feel free to use the code for your own project.

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

### Development server

1. Install [Docker](https://www.docker.com/products/docker-desktop) and [Bun](https://bun.sh)
2. Run `cd docker` to enter the docker folder
3. Run `bun install` to install the dependencies
4. Run `bun dev` to start the server
5. Open your browser and go to `http://localhost:6543`

### Development server on Windows

1. Install [Docker](https://www.docker.com/products/docker-desktop)
2. Run `cd docker` to enter the docker folder
3. Run the image `docker run --rm -it -e PORT=6543 -p 6543:6543 -v .:/app thgh/autoeagler-webserver bun dev`
4. Open your browser and go to `http://localhost:6543`

### Publish to Docker Hub

1. Run `docker buildx build . -t thgh/autoeagler-webserver --platform=linux/amd64,linux/arm64/v8 --push` to build and push the docker image
2. Run `bun drun` to test if the docker image is working

# For Mojang:

This tool does **NOT** include any of the source code from Minecraft, MCP, or any other illegal/copyrighted resources, nor any info on how to get it.
