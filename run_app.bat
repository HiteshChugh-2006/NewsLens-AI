@echo off
title NewsLens AI - Launching Server...
cd /d "%~dp0"
echo ========================================================
echo Starting NewsLens AI Web Application...
echo Local Server: http://localhost:8501
echo ========================================================
".venv\Scripts\streamlit.exe" run app.py
pause
