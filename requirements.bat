@echo off
python create_venv.py
start "create_venv.exe"
call venv\Scripts\activate
pip install -r requirements.txt

setlocal enableextensions enabledelayedexpansion

set "url1=https://github.com/ffbinaries/ffbinaries-prebuilt/releases/download/v4.4.1/ffplay-4.4.1-win-64.zip"
set "file1=ffplay-4.4.1-win-64.zip"

set "url2=https://github.com/ffbinaries/ffbinaries-prebuilt/releases/download/v4.4.1/ffprobe-4.4.1-win-64.zip"
set "file2=ffprobe-4.4.1-win-64.zip"

set "url3=https://github.com/ffbinaries/ffbinaries-prebuilt/releases/download/v4.4.1/ffmpeg-4.4.1-win-64.zip"
set "file3=ffmpeg-4.4.1-win-64.zip"

if not exist "%file1%" (
    echo Downloading %file1%...
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%url1%', '%file1%')"
    echo Extracting %file1%...
    powershell -Command "Expand-Archive -Path '%file1%' -DestinationPath . -Force"
)

if not exist "%file2%" (
    echo Downloading %file2%...
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%url2%', '%file2%')"
    echo Extracting %file2%...
    powershell -Command "Expand-Archive -Path '%file2%' -DestinationPath . -Force"
)

if not exist "%file3%" (
    echo Downloading %file3%...
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%url3%', '%file3%')"
    echo Extracting %file3%...
    powershell -Command "Expand-Archive -Path '%file3%' -DestinationPath . -Force"
)

echo Done.
pause
