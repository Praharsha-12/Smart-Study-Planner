@echo off
cd /d "%~dp0"
start "StudySync Website" python main.py
echo Waiting for the website to become ready...
powershell -NoProfile -Command "for ($i=0; $i -lt 20; $i++) { try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:5000' -UseBasicParsing -TimeoutSec 2; if ($r.StatusCode -eq 200) { exit 0 } } catch {}; Start-Sleep -Seconds 1 }; exit 1"
if %errorlevel% equ 0 (
  start "" "http://127.0.0.1:5000"
)
