@echo off

title AutoEagler

set LatestBungee="https://ci.md-5.net/job/BungeeCord/lastSuccessfulBuild/artifact/bootstrap/target/BungeeCord.jar"
set BungeeLocation="./Bungee/BungeeCord.jar"
set LatestEaglerX="https://raw.githubusercontent.com/lax1dude/eagl3rxbungee-memory-leak-patch/main/EaglerXBungee-Memleak-Fixed.jar"
set EaglerXLocation="./Bungee/Plugins/eaglerXbungee.jar"
set LatestSpigot="https://cdn.getbukkit.org/spigot/spigot-1.8.8-R0.1-SNAPSHOT-latest.jar"
set SpigotLocation="./Server/Spigot.jar"

:menu
ver > nul
cls
echo 1) Set up AutoEagler
echo 2) Run AutoEagler
echo 3) Add plugins
echo 4) Wipe everything
echo 5) Exit
echo.
choice /c 123456 /N /M ">> "

if %errorlevel% == 1 goto :AutoEagler
if %errorlevel% == 2 goto :run
if %errorlevel% == 3 goto :menu
if %errorlevel% == 4 goto :menu
if %errorlevel% == 5 goto exit 0
if %errorlevel% == 6 goto :autoreplace

:AutoEagler
cls

:bungee
if exist Bungee/NUL (goto :eagx)
mkdir Bungee
echo Pulling latest BungeeCord.jar
curl --output %BungeeLocation% --url %LatestBungee% -s
echo BungeeCord.jar downloaded to %BungeeLocation%

:eagx
if exist Bungee/plugins/NUL (goto :spigot)
cd Bungee
mkdir plugins
cd ..
echo Pulling EaglerXbungee.jar
curl --output %EaglerXLocation% --url %LatestEaglerX% -s
echo eaglerxbungee.jar downloaded to %EaglerXLocation%

:spigot
if exist Server/NUL (goto :initialRun)
mkdir Server
echo Pulling 1.8.8 Spigot.jar
curl --output %SpigotLocation% --url %LatestSpigot% -s
echo Spigot.jar downloaded to %SpigotLocation%
pause


:initialRun 
cls
echo Generating BungeeCord config files
start /min cmd.exe /C "title bungee && cd Bungee && java -Xms64M -Xmx64M -jar BungeeCord.jar"
start /min cmd.exe /C "title spigot && cd Server && java -Xms1G -Xmx1G -jar Spigot.jar"
timeout 10 > nul
taskkill /IM cmd.exe /FI "WINDOWTITLE eq bungee*" >nul 2>&1

:setupEnd
cls
echo Changing Spigot's eula to true
set search=false
set replace=true
for /F "delims=" %%a in (Server/eula.txt) DO (
   set line=%%a
   setlocal EnableDelayedExpansion
   >> Server/output.txt echo(!line:%search%=%replace%!
   endlocal
)
cd Server
del /Q eula.txt
ren output.txt eula.txt
cd ..

:initialSpigot
cls
echo Generating Spigot config files
start /min cmd.exe /C "title spigot && cd Server && java -Xms1G -Xmx1G -jar Spigot.jar"
timeout 15 > nul
taskkill /IM cmd.exe /FI "WINDOWTITLE eq spigot*" >nul 2>&1
cls
echo Done
goto :menu

:run
cls
start /min cmd.exe /C "title bungee && cd Bungee && java -Xms64M -Xmx64M -jar BungeeCord.jar"
start /min cmd.exe /C "title spigot && cd Server && java -Xms1G -Xmx1G -jar Spigot.jar"

:shutdown
ver > nul
cls
echo Starting servers...
timeout 15 > nul
cls
echo Servers running...
echo Press any key to stop them
pause > nul
choice /C YN /N /M "Are you sure you want to shutdown the servers? [Y/N]"
if %errorlevel% == 1 echo Stopping servers ...
if %errorlevel% == 2 goto :shutdown
taskkill /IM cmd.exe /FI "WINDOWTITLE eq bungee*" >nul 2>&1
taskkill /IM cmd.exe /FI "WINDOWTITLE eq spigot*" >nul 2>&1
goto :menu