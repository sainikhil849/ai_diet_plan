@echo off
echo ============================================================
echo AI-NutriCare API Server
echo ============================================================
echo.
echo Starting server...
echo.

cd /d %~dp0
python run_server.py

pause
