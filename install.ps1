$ErrorActionPreference = "Stop"

$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallDir = Join-Path $env:LOCALAPPDATA "unified TREE"
$StartMenu = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Copy-Item "$SourceDir\server.py", "$SourceDir\desktop.py", "$SourceDir\devices.json", "$SourceDir\platform.json" -Destination $InstallDir -Force
Copy-Item "$SourceDir\web", "$SourceDir\protocol" -Destination $InstallDir -Recurse -Force

$Launcher = Join-Path $InstallDir "unified-tree.cmd"
@"
@echo off
where pyw >nul 2>nul && (start "" pyw "$InstallDir\desktop.py" & exit /b)
where pythonw >nul 2>nul && (start "" pythonw "$InstallDir\desktop.py" & exit /b)
echo Python 3 is required. Install it from https://www.python.org/downloads/
pause
"@ | Set-Content -Path $Launcher -Encoding ASCII

$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut((Join-Path $StartMenu "unified TREE.lnk"))
$Shortcut.TargetPath = $Launcher
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Description = "Control plane for interconnected SoC device nodes"
$Shortcut.Save()

Write-Host "unified TREE is installed in $InstallDir"
Write-Host "Open unified TREE from the Windows Start menu."
