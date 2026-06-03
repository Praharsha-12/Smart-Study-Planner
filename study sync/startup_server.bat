@echo off
:: StudySync Auto-Start Script
:: Place this in Windows Startup folder for automatic startup
:: Location: C:\Users\praha\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

cd /d "c:\Users\praha\Desktop\study sync"

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python.
    exit /b 1
)

:: Install dependencies
echo Installing/updating dependencies...
python -m pip install -q -r requirements.txt

:: Start the web server
echo Starting StudySync web server...
start "StudySync Web Server" cmd /k "title StudySync Server - Keep this window open & python web.py"

:: Wait a moment for server to start
timeout /t 3 /nobreak

:: Open website
start "" "http://127.0.0.1:5000"

echo Server started successfully!
