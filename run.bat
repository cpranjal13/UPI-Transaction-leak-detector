@echo off
title UPI Leak Detector
cd /d "%~dp0"
echo ===================================================
echo             UPI LEAK DETECTOR SERVER
echo ===================================================
echo.
echo Starting Flask Application...
echo Local Link: http://localhost:5000
echo.
start "" "http://localhost:5000"
"%~dp0.venv\Scripts\python.exe" "%~dp0app.py"
pause
