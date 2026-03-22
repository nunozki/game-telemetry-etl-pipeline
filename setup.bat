@echo off
title Setup - Steam Telemetry ETL
echo ===================================================
echo    Steam Telemetry ETL Pipeline - Environment Setup
echo ===================================================
echo.

:: 1. Check if Python is installed
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to your PATH environment variable.
    echo Please install Python 3.x from https://www.python.org/downloads/
    pause
    exit /b
)
echo -- Python found!
echo.

:: 2. Create the Virtual Environment (venv)
echo [2/4] Creating Virtual Environment (venv)...
if not exist "venv\" (
    python -m venv venv
    echo -- Virtual Environment successfully created.
) else (
    echo -- Virtual Environment already exists. Skipping this step...
)
echo.

:: 3. Activate the Virtual Environment
echo [3/4] Activating the Virtual Environment...
call venv\Scripts\activate
echo.

:: 4. Install dependencies
echo [4/4] Upgrading pip and installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install pandas requests
echo.

echo ===================================================
echo    SETUP COMPLETED SUCCESSFULLY!
echo ===================================================
echo.
echo To run the pipeline, you first need to activate the environment.
echo You can do this by running this command in your terminal:
echo venv\Scripts\activate
echo.
echo Then, simply run:
echo python main.py
echo.
pause