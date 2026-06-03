Set-Location -Path $PSScriptRoot
Write-Host "Installing dependencies..."
python -m pip install -r requirements.txt
Write-Host "Starting StudySync website..."
python web.py
