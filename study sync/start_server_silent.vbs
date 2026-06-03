Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Change to the script directory
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
objShell.CurrentDirectory = strScriptPath

' Run the batch file silently (no visible window)
strCommand = """" & strScriptPath & "\startup_server.bat"""
objShell.Run strCommand, 0, False

' Show a notification
Set objShell = Nothing
