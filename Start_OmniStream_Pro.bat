@echo off
title OmniStream Pro
cd /d "%~dp0"
python main_gui.py
if %errorlevel% neq 0 (
    echo.
    echo OmniStream Pro failed to start. Running dependencies check...
    python setup_dependencies.py
    pause
)
