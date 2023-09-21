#!/bin/bash

echo "AutoEagler"

LatestBungee="https://ci.md-5.net/job/BungeeCord/lastSuccessfulBuild/artifact/bootstrap/target/BungeeCord.jar"
BungeeLocation="./Bungee/BungeeCord.jar"
LatestEaglerX="https://raw.githubusercontent.com/lax1dude/eagl3rxbungee-memory-leak-patch/main/EaglerXBungee-Memleak-Fixed.jar"
EaglerXLocation="./Bungee/Plugins/eaglerXbungee.jar"
LatestSpigot="https://cdn.getbukkit.org/spigot/spigot-1.8.8-R0.1-SNAPSHOT-latest.jar"
SpigotLocation="./Server/Spigot.jar"

menu() {
    clear
    echo "1) Set up AutoEagler"
    echo "2) Run AutoEagler"
    echo "3) Add plugins"
    echo "4) Wipe everything"
    echo "5) Exit"
    echo ""
    read -p ">> " choice

    case $choice in
        1) AutoEagler ;;
        2) run ;;
        3) menu ;;
        4) menu ;;
        5) exit 0 ;;
        6) autoreplace ;;
        *) menu ;;
    esac
}

AutoEagler() {
    clear

    bungee() {
        if [ -d "Bungee" ]; then
            eagx
        else
            mkdir Bungee
            echo "Pulling latest BungeeCord.jar"
            curl --output "$BungeeLocation" --url "$LatestBungee" -s
            echo "BungeeCord.jar downloaded to $BungeeLocation"
            eagx
        fi
    }

    eagx() {
        if [ -d "Bungee/plugins" ]; then
            spigot
        else
            cd Bungee
            mkdir plugins
            cd ..
            echo "Pulling EaglerXbungee.jar"
            curl --output "$EaglerXLocation" --url "$LatestEaglerX" -s
            echo "eaglerxbungee.jar downloaded to $EaglerXLocation"
            spigot
        fi
    }

    spigot() {
        if [ -d "Server" ]; then
            initialRun
        else
            mkdir Server
            echo "Pulling 1.8.8 Spigot.jar"
            curl --output "$SpigotLocation" --url "$LatestSpigot" -s
            echo "Spigot.jar downloaded to $SpigotLocation"
            read -p "Press Enter to continue..."
            initialRun
        fi
    }

    initialRun() {
        clear
        echo "Generating BungeeCord config files"
        (cd Bungee && java -Xms64M -Xmx64M -jar BungeeCord.jar) > /dev/null 2>&1 &
        (cd Server && java -Xms1G -Xmx1G -jar Spigot.jar) > /dev/null 2>&1 &
        sleep 10
        pkill -f "java -Xms64M -Xmx64M -jar BungeeCord.jar"
        sed -i 's/eula=false/eula=true/' Server/eula.txt
        clear
        echo "Done"
        read -p "Press Enter to continue..."
        initialSpigot
    }

    setupEnd() {
        clear
        echo "Changing Spigot's eula to true"
        search="false"
        replace="true"
        while IFS= read -r line; do
            echo "${line//$search/$replace}" >> Server/output.txt
        done < Server/eula.txt

        mv Server/output.txt Server/eula.txt

        initialSpigot
    }

    initialSpigot() {
        clear
        echo "Generating Spigot config files"
        (cd Server && java -Xms1G -Xmx1G -jar Spigot.jar) > /dev/null 2>&1 &
        sleep 15
        pkill -f "java -Xms1G -Xmx1G -jar Spigot.jar"
        clear
        echo "Done"
        read -p "Press Enter to continue..."
        menu
    }

    bungee
}

run() {
    clear
    (cd Bungee && java -Xms64M -Xmx64M -jar BungeeCord.jar) > /dev/null 2>&1 &
    (cd Server && java -Xms1G -Xmx1G -jar Spigot.jar) > /dev/null 2>&1 &
    shutdown
}

shutdown() {
    clear
    echo "Starting servers..."
    sleep 15
    clear
    echo "Servers running..."
    read -n 1 -p "Press CTRL+C key to stop"
    echo ""
#    read -p "Are you sure you want to shutdown the servers? [Y/N]" choice
#    case $choice in
#        Y|y) echo "Stopping servers..."
#             pkill -f "java -Xms64M -Xmx64M -jar BungeeCord.jar"
#             pkill -f "java -Xms1G -Xmx1G -jar Spigot.jar"
#             menu ;;
#        *) shutdown ;;
#    esac
}

menu
