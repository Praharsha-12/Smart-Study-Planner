@echo off
cd /d "%~dp0"
echo Installing dependencies...
python -m pip install -r requirements.txt
echo Launching StudySync website...
start "StudySync Server" python web.py
echo Waiting for the website to become ready...
powershell -NoProfile -Command "for ($i=0; $i -ltclose vs code 20; $i++) { try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:5000' -UseBasicParsing -TimeoutSec 2; if ($r.StatusCode -eq 200) { exit 0 } } catch {}; Start-Sleep -Seconds 1 }; exit 1"
if %errorlevel% equ 0 (
  start "" "http://127.0.0.1:5000"
) else (
  echo Failed to reach http://127.0.0.1:5000 after waiting.
  echo Please open the browser manually after the server starts.
  pause
)
