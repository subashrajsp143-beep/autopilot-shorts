@echo off
title MiniTalesWorld - YouTube Token Refresh
color 0A
echo ============================================================
echo   MiniTalesWorld YouTube Token Refresh
echo ============================================================
echo.
echo Launching YouTube Authorization in your browser...
echo.
cd /d "C:\Users\Subhash Kumar\.gemini\antigravity\scratch\autopilot_shorts"
"C:\Users\Subhash Kumar\AppData\Local\Python\bin\python.exe" scripts\reauth_youtube.py
echo.
echo ============================================================
echo Process completed! You can close this window.
echo ============================================================
pause
