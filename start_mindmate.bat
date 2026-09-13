@echo off
title MindMate AI - Startup
echo ====================================================
echo Starting MindMate AI - Mental Wellness Application...
echo ====================================================
echo.

cd /d "%~dp0"

echo Opening browser at http://127.0.0.1:8000 ...
start http://127.0.0.1:8000

echo Starting Backend Server on http://127.0.0.1:8000 ...
python backend/main.py

pause
