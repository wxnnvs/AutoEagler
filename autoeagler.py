import os
from wsgiref.simple_server import server_version
import requests
import shutil
import time
import subprocess
import os
import logging
from datetime import datetime
import json

from contextlib import redirect_stdout, redirect_stderr
from pyngrok import conf, ngrok
import psutil
import platform
if platform.system() == 'Windows':
    import pygetwindow as gw


#create log files
log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log.txt")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
    ]
)
logging.info("Autoeagler v2.3 logs")
logging.info("starting Autoeagler...")



# URLs and file locations
latest_bungee_1_8_8 = "https://api.papermc.io/v2/projects/waterfall/versions/1.20/builds/556/downloads/waterfall-1.20-556.jar"
bungee_location_1_8_8 = "Bungee-1.8.8/BungeeCord.jar"
latest_eaglerx_1_8_8 = "https://github.com/lax1dude/eagl3rxbungee-memory-leak-patch/raw/main/EaglerXBungee-Memleak-Fixed.jar"
eaglerx_location_1_8_8 = "./Bungee-1.8.8/plugins/eaglerXbungee.jar"
latest_spigot_1_8_8 = "https://cdn.getbukkit.org/spigot/spigot-1.8.8-R0.1-SNAPSHOT-latest.jar"
spigot_location_1_8_8 = "Server-1.8.8/Spigot.jar"
# NOTE: eaglerbungee 1.5.2 is NOT a bungeecord plugin. its regular BungeeCord except it accepts WebSockets instead of raw TCP connections
latest_eaglerbungee_1_5_2 = "https://git.eaglercraft.online/eaglercraft/eaglercraft-builds/raw/branch/main/java/Eaglercraft_1.5.2_Service_Pack_1.01/bungee_command/bungee-dist.jar"
eaglerbungee_location_1_5_2 = "Bungee-1.5.2/BungeeCord.jar"
# these files are required for eaglerbungee 1.5.2 to function(specially config.yml)
file1_1_5_2 = "https://git.eaglercraft.online/eaglercraft/eaglercraft-builds/raw/branch/main/java/Eaglercraft_1.5.2_Service_Pack_1.01/bungee_command/bans.txt"
file1_location_1_5_2 = "Bungee-1.5.2/bans.txt"
file2_1_5_2 = "https://git.eaglercraft.online/eaglercraft/eaglercraft-builds/raw/branch/main/java/Eaglercraft_1.5.2_Service_Pack_1.01/bungee_command/config.yml"
file2_location_1_5_2 = "Bungee-1.5.2/config.yml"
file3_1_5_2 = "https://git.eaglercraft.online/eaglercraft/eaglercraft-builds/raw/branch/main/java/Eaglercraft_1.5.2_Service_Pack_1.01/bungee_command/server-icon.png"
file3_location_1_5_2 = "Bungee-1.5.2/server-icon.png"
latest_spigot_1_5_2 = "https://cdn.getbukkit.org/spigot/spigot-1.5.2-R1.1-SNAPSHOT.jar"
spigot_location_1_5_2 = "server-1.5.2/Spigot.jar"
#1.3 beta
latest_bukkit_1_3 = "https://git.eaglercraft.rip/eaglercraft/eaglercraft-builds/raw/branch/main/Eaglercraft_b1.3_Bukkit/eaglercraft-bukkit.jar"
bukkit_location_1_3 = "server-beta-1.3/eaglercraft-bukkit.jar"
file1_1_3 = "https://git.eaglercraft.rip/eaglercraft/eaglercraft-builds/raw/branch/main/Eaglercraft_b1.3_Bukkit/eagler.yml"
file1_location_1_3 = "server-beta-1.3/eagler.yml"
file2_1_3 = "https://git.eaglercraft.rip/eaglercraft/eaglercraft-builds/raw/branch/main/Eaglercraft_b1.3_Bukkit/server.properties"
file2_location_1_3 = "server-beta-1.3/server.properties"

token = ""

def close_terminal_window(window_name):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if window_name in proc.info['cmdline']:
            try:
                proc.terminate()
                print(f"Window '{window_name}' terminated successfully.")
            except psutil.NoSuchProcess:
                print(f"Failed to terminate window '{window_name}'. Process not found.")
def download_file(url, location):
    logging.info(f"downloaded a file from {url} to {location}")
    response = requests.get(url)
    with open(location, 'wb') as file:
        file.write(response.content)

def replace_in_file(file_path, search, replace):
    with open(file_path, 'r') as file:
        file_data = file.read()
    file_data = file_data.replace(search, replace)
    with open(file_path, 'w') as file:
        file.write(file_data)

def set_authtoken(token):
    # Load the JSON data from the file
    with open('config.json', 'r') as file:
        config_data = json.load(file)

    config_data['token'] = token

    # Save the updated JSON data back to the file
    with open('config.json', 'w') as file:
        json.dump(config_data, file, indent=4)

def get_authtoken():
    global token
    # Load the JSON data from the file
    with open('config.json', 'r') as file:
        config_data = json.load(file)

    # Read the value of the "token" field into a variable
    token = config_data.get('token', None)

def remove_everything():
    clear_screen()
    sure = input("All progress made in-game will be lost\nAre you sure you want to remove all files? (Y/N)\n>> ")
    if sure.lower() == "y":
        shutil.rmtree("./Bungee-1.8.8", ignore_errors=True)
        shutil.rmtree("./Server-1.8.8", ignore_errors=True)
        shutil.rmtree("./Bungee-1.5.2", ignore_errors=True)
        shutil.rmtree("./Server-1.5.2", ignore_errors=True)
        shutil.rmtree("./Server-beta-1.3", ignore_errors=True)
        if os.path.exists(bungee_location_1_8_8):
            os.remove(bungee_location_1_8_8)
        if os.path.exists(eaglerx_location_1_8_8):
            os.remove(eaglerx_location_1_8_8)
        if os.path.exists(spigot_location_1_8_8):
            os.remove(spigot_location_1_8_8)
        print("All server files have been deleted!")
        logging.info("removed everything D:")
    else:
        pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_command_in_new_terminal(command):
    if os.name == 'nt':
        subprocess.Popen(['start', 'cmd', '/c', command], shell=True)
    elif os.name == 'posix':
        try:
            subprocess.Popen(['xdg-open', 'x-terminal-emulator', '--', 'bash', '-c', command])
        except FileNotFoundError:
            print("No suitable terminal emulator found. Please run the command manually.")
    else:
        print("Unsupported operating system for running commands in a new terminal.")


def run_servers(server_version):
    
    clear_screen()

    if server_version == "0" :
        logging.info("starting bungeecord 1.8.8 ...")
        # Change directory to the location of BungeeCord.jar
        os.chdir(os.path.dirname(bungee_location_1_8_8))
        run_command_in_new_terminal(f'title bungee 1.8.8 & java -Xms64M -Xmx64M -jar {os.path.basename(bungee_location_1_8_8)}')
        os.chdir(os.path.dirname("../"))
        logging.info("starting spigot 1.8.8 ...")
        # Change directory to the location of Spigot.jar
        os.chdir(os.path.dirname(spigot_location_1_8_8))
        run_command_in_new_terminal(f'title spigot 1.8.8 & java -Xms2G -Xmx2G -jar {os.path.basename(spigot_location_1_8_8)}')
        os.chdir(os.path.dirname("../"))
    if server_version == "1" :
        logging.info("starting bungeecord 1.5.2 ...")
            # Change directory to the location of BungeeCord.jar
        os.chdir(os.path.dirname(eaglerbungee_location_1_5_2))
        run_command_in_new_terminal(f'title bungee 1.5.2 & java -Xmx32M -Xms32M -jar {os.path.basename(eaglerbungee_location_1_5_2)}')
        os.chdir(os.path.dirname("../"))
        logging.info("starting spigot 1.5.2 ...")
        # Change directory to the location of Spigot.jar
        os.chdir(os.path.dirname(spigot_location_1_5_2))
        run_command_in_new_terminal(f'title spigot 1.5.2 & java -Xms2G -Xmx2G -jar {os.path.basename(spigot_location_1_5_2)}')
        os.chdir(os.path.dirname("../"))
    if server_version == "2" :
        # Change directory to the location of bukkit.jar
        os.chdir(os.path.dirname(bukkit_location_1_3))
        run_command_in_new_terminal(f'title eaglerbukkit beta 1.3 & java -Xms2G -Xmx2G -jar {os.path.basename(bukkit_location_1_3)}')
        os.chdir(os.path.dirname("../"))

    print("Servers starting ...")

def stop_servers():
    print("Stopping servers...")
    logging.info("stopping servers...")

    
    if platform.system() == 'Windows':
        for window in gw.getAllTitles():
            if 'bungee' in window.lower() or 'spigot' in window.lower() or 'eaglerbukkit' in window.lower():
                try:
                    gw.getWindowsWithTitle(window)[0].close()
                    print(f"Closed {window}")
                except Exception as e:
                    print(f"Failed to close {window}. Error: {e}")
    elif platform.system() == 'Linux':
        close_terminal_window('bungee')
        close_terminal_window('spigot')
        if server_version == "2":
            close_terminal_window('eaglerbukkit')
    logging.info("servers stopped")
    print("servers stopped")

def ngrok_start(server_version):
    global http_tunnel

    clear_screen()

    #ask for region to use
    ligma = input("What region would u like to use for your server? \nap -> Asia/Pacific (Singapore)\nau -> Australia (Sydney)\neu -> Europe (Frankfurt)\nin -> India (Mumbai)\njp -> Japan (Tokyo)\nsa -> South America (São Paulo)\nus -> United States (Ohio)\nus-cal-1 -> United States (California)\n>> ")
    conf.get_default().region = ligma

    run_servers(server_version)

    #open tunnel to NGROK
    conf.get_default().monitor_thread = False
    with redirect_stdout(None) and redirect_stderr(None):
        http_tunnel = ngrok.connect(8081, 'http', bind_tls=True)
    logging.info(f"Server running at {http_tunnel.public_url.replace('https', 'wss')}")
    print(f"Server running at {http_tunnel.public_url.replace('https', 'wss')}")

def main():
    global token
    get_authtoken()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("1) Set up AutoEagler")
        print("2) Run locally")
        print("3) Run with NGROK")
        print("4) Wipe everything")
        print("5) Exit")
        print("6) start web dashboard (soon)")

        choice = input(">> ")

        if choice == '1':
            logging.info('user chose "1) Set up AutoEagler"')
            clear_screen()
            #ask for NGROK authtoken
            token = input("Please input your NGROK authtoken.\nRetrieve it at https://dashboard.ngrok.com/get-started/your-authtoken\n>> ")
            conf.get_default().auth_token = token
            set_authtoken(token)

            clear_screen()

            #Ask for version
            version = str(input("What version of eaglercraft would you like to make your server for?\n0 -> 1.8.8(u19)\n1 -> 1.5.2\n2 -> beta 1.3\n>> "))
            logging.info(f"User chose {version}")

            clear_screen()

            #Ask for gamemode
            if not version == "2": # bc you cant change your gamemode on beta 1.3 :skull:
                gamemode = str(input("What gamemode would you like to use?\n0 -> Survival\n1 -> Creative\n2 -> Adventure\n3 -> Spectator\n>> "))
                hardcore = "false"
                if gamemode == "0":
                    logging.info("user chose survival mode")
                    if input("Do you want to enable hardcore? (Y/N)\n>> ").lower() == "y":
                        hardcore = "true"
                        logging.info("user chose hardcore mode after choosing survival")
                if gamemode == "1":
                    logging.info("user chose creative mode")
                
                if gamemode == "2":
                    logging.info("user chose adventure mode")

                if gamemode == "3":
                    logging.info("user chose spectator mode")

            clear_screen()

            #Ask for seed
            if not version == "2" : # bc you cant change the seed on beta 1.3 :skull:
                seed = str(input("What seed would you like to use?\n(Leave empty for a random seed)\n>> "))

            clear_screen()
            if version == "0":
                if not os.path.exists(bungee_location_1_8_8):
                    os.makedirs(os.path.dirname(bungee_location_1_8_8), exist_ok=True)
                    download_file(latest_bungee_1_8_8, bungee_location_1_8_8)
                    print(f"BungeeCord.jar downloaded to {bungee_location_1_8_8}")

                if not os.path.exists(eaglerx_location_1_8_8):
                    os.makedirs(os.path.dirname(eaglerx_location_1_8_8), exist_ok=True)
                    download_file(latest_eaglerx_1_8_8, eaglerx_location_1_8_8)
                    print(f"Eaglerxbungee.jar downloaded to {eaglerx_location_1_8_8}")

                if not os.path.exists(spigot_location_1_8_8):
                    os.makedirs(os.path.dirname(spigot_location_1_8_8), exist_ok=True)
                    download_file(latest_spigot_1_8_8, spigot_location_1_8_8)
                    print(f"Spigot.jar downloaded to {spigot_location_1_8_8}")
            if version == "1":
                if not os.path.exists(eaglerbungee_location_1_5_2):
                    os.makedirs(os.path.dirname(eaglerbungee_location_1_5_2), exist_ok=True)
                    download_file(latest_eaglerbungee_1_5_2, eaglerbungee_location_1_5_2)
                    print(f"BungeeCord.jar downloaded to {eaglerbungee_location_1_5_2}")

                if not os.path.exists(file1_location_1_5_2):
                    os.makedirs(os.path.dirname(file1_location_1_5_2), exist_ok=True)
                    download_file(file1_1_5_2, file1_location_1_5_2)
                    print(f"bans.txt downloaded to {file1_location_1_5_2}")
                    
                if not os.path.exists(file2_location_1_5_2):
                    os.makedirs(os.path.dirname(file2_location_1_5_2), exist_ok=True)
                    download_file(file2_1_5_2, file2_location_1_5_2)
                    print(f"config.yml downloaded to {file2_location_1_5_2}")
                                        
                if not os.path.exists(file3_location_1_5_2):
                    os.makedirs(os.path.dirname(file3_location_1_5_2), exist_ok=True)
                    download_file(file3_1_5_2, file3_location_1_5_2)
                    print(f"server-icon.png downloaded to {file3_location_1_5_2}")

                if not os.path.exists(spigot_location_1_5_2):
                    os.makedirs(os.path.dirname(spigot_location_1_5_2), exist_ok=True)
                    download_file(latest_spigot_1_5_2, spigot_location_1_5_2)
                    print(f"Spigot.jar downloaded to {spigot_location_1_5_2}")
            if version == "2":
                if not os.path.exists(bukkit_location_1_3):
                    os.makedirs(os.path.dirname(bukkit_location_1_3), exist_ok=True)
                    download_file(latest_bukkit_1_3, bukkit_location_1_3)
                    print(f"bukkit.jar downloaded to {bukkit_location_1_3}")

                if not os.path.exists(file1_location_1_3):
                    os.makedirs(os.path.dirname(file1_location_1_3), exist_ok=True)
                    download_file(file1_1_3, file1_location_1_3)
                    print(f"eagler.yml downloaded to {file1_location_1_3}")
                    
                if not os.path.exists(file2_location_1_3):
                    os.makedirs(os.path.dirname(file2_location_1_3), exist_ok=True)
                    download_file(file2_1_3, file2_location_1_3)
                    print(f"server.properties downloaded to {file2_location_1_3}")
            
            print("Initial run..")

            run_servers(version)  # Run the servers after downloading
            time.sleep(15)
            stop_servers()

            
            if version == "0" : 
                print("Enabling EULA in spigot...")
                logging.info("Enabling EULA in spigot...")
                replace_in_file("Server-1.8.8/eula.txt", "false", "true")  # Change eula to true
                run_servers(version)
                time.sleep(15)
                stop_servers()
                
            print("Generating config files...")
            logging.info("Generating config files...")
            if version == "0" : 
                print("Modifiying 1.8.8 config files...")
                # Replace content in configuration files
                replace_in_file("Server-1.8.8/server.properties", "online-mode=true", "online-mode=false")
                replace_in_file("Server-1.8.8/spigot.yml", "bungeecord: false", "bungeecord: true")
                replace_in_file("Bungee-1.8.8/plugins/EaglercraftXBungee/authservice.yml", "enable_authentication_system: true", "enable_authentication_system: false")
                replace_in_file("Bungee-1.8.8/plugins/EaglercraftXBungee/settings.yml", "server_name: 'EaglercraftXBungee Server'", "server_name: 'AutoEagler Server'")
                replace_in_file("Bungee-1.8.8/plugins/EaglercraftXBungee/listeners.yml", "&6An EaglercraftX server", "&6An AutoEagler server")

                replace_in_file("Bungee-1.8.8/config.yml", "online_mode: true", "online_mode: false")
                replace_in_file("Bungee-1.8.8/config.yml", "ip_forward: false", "ip_forward: true")

                #Custom settings
                replace_in_file("Server-1.8.8/server.properties", "gamemode=0", "gamemode="+gamemode)
                replace_in_file("Server-1.8.8/server.properties", "hardcore=false", "hardcore="+hardcore)

                if not seed == "":
                    replace_in_file("Server-1.8.8/server.properties", "seed=", "seed="+seed)
            if version == "1" :
                logging.info("Modifiying 1.5.2 config files...")
                # Replace content in configuration files
                replace_in_file("Server-1.5.2/server.properties", "online-mode=true", "online-mode=false")
                replace_in_file("Server-1.5.2/spigot.yml", "bungeecord: false", "bungeecord: true")
                replace_in_file("Bungee-1.5.2/config.yml", "server_name: EaglercraftBungee Server", "server_name: AutoEagler Server")
                replace_in_file("Bungee-1.5.2/config.yml", "&6An Eaglercraft server", "&6An AutoEagler server")
                replace_in_file("Bungee-1.5.2/config.yml", "forward_ip: false", "forward_ip: true")
                replace_in_file("Bungee-1.5.2/config.yml", "host: 0.0.0.0:25565", "host: 0.0.0.0:8081")
                replace_in_file("Bungee-1.5.2/config.yml", "address: localhost:25569", "address: localhost:25565")

                #Custom settings
                replace_in_file("Server-1.5.2/server.properties", "gamemode=0", "gamemode="+gamemode)
                replace_in_file("Server-1.5.2/server.properties", "hardcore=false", "hardcore="+hardcore)

                if not seed == "":
                    replace_in_file("Server-1.5.2/server.properties", "seed=", "seed="+seed)
            if version == "2" :
                logging.info("Modifiying beta 1.3 config files...")
                # Replace content in configuration files
                replace_in_file("Server-beta-1.3/eagler.yml", "only_allow_registered_users_to_login: true", "only_allow_registered_users_to_login: false")
                replace_in_file("Server-beta-1.3/eagler.yml", "allow_self_registration: false", "allow_self_registration: true")
                replace_in_file("Server-beta-1.3/eagler.yml", "allow_self_registration_without_expiration: false", "allow_self_registration_without_expiration: true")
                replace_in_file("Server-beta-1.3/server.properties", "max-players=20", "max-players=69420")
                replace_in_file("Server-beta-1.3/server.properties", "websocket-address=0.0.0.0\:25565", "websocket-address=0.0.0.0\:8081")

            clear_screen()
            print("You're done setting up AutoEagler\nRun the servers by using option 2 and close them using 5")
            logging.info("Finished setting up Autoeagler")
            time.sleep(3)

        elif choice == '2':
            clear_screen()
            logging.info('user chose "2) Run locally"')
            version = str(input("What version of eaglercraft would you like to run?\nNOTE: you can only run the versions you set up!\n0 -> 1.8.8(u19)\n1 -> 1.5.2\n2 -> beta 1.3\n>> "))
            run_servers(version)
            if not version == "2":
                print("Server running at ws://localhost:8081")
                input("Press [Enter] to return to the menu (servers stay up)")
            else :
                print("Server running at 127.0.0.1:8081\nUse /register-password <password> when you join the server to set your password!")
                input("Press [Enter] to return to the menu (servers stay up)") 

        elif choice == '3':
            clear_screen()
            logging.info('user chose "3) Run with NGROK"')
            conf.get_default().auth_token = token
            version = str(input("What version of eaglercraft would you like to run?\nNOTE: you can only run the versions you set up!\n0 -> 1.8.8(u19)\n1 -> 1.5.2\n2 -> beta 1.3\n>> "))
            ngrok_start(version)
            if not version == "2":
                input("Press [Enter] to return to the menu (servers stay up)")
            else:
                print("Use /register-password <password> when you join the server to set your password!")
                input("Press [Enter] to return to the menu (servers stay up)") 


        elif choice == '4':
            logging.info('user chose "4) Wipe everything"')
            remove_everything()
            print("Everything has been removed.")

        elif choice == '5':
            logging.info('user chose "5) Exit"')
            conf.get_default().auth_token = token
            stop_servers()
            logging.info("exiting Autoeagler...")
            with redirect_stdout(None) and redirect_stderr(None):
                tunnels = ngrok.get_tunnels()
            if not tunnels:
                break
            else:
                ngrok.disconnect(http_tunnel.public_url)
                break

if __name__ == "__main__":
    main()
