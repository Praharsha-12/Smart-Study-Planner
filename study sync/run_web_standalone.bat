@echo off
:: This script runs the web server in a minimized window that persists independently
:: It will keep running even if VS Code or any terminal is closed

cd /d "%~dp0"
echo Installing dependencies...
python -m pip install -r requirements.txt

echo Launching StudySync website (running independently)...
:: Start in a separate process that won't be tied to this terminal
start "" /MIN cmd /c "title StudySync Server & python web.py & pause"

echo Server started! It will continue running even if you close this window.
echo.
echo Opening website in browser...
timeout /t 3 /nobreak

:: Open browser
start "" "http://127.0.0.1:5000"

echo Done! Website is running on http://127.0.0.1:5000
pause
