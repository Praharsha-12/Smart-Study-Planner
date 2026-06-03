# Run this in PowerShell as Administrator to set up the scheduled task
# Usage: powershell -ExecutionPolicy Bypass -File start_server.ps1

$taskName = "StudySync Web Server"
$taskPath = "c:\Users\praha\Desktop\study sync\run_web.bat"

# Create a scheduled task that runs at startup
$action = New-ScheduledTaskAction -Execute $taskPath
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force

Write-Host "Scheduled task '$taskName' created! Server will start automatically at startup."
