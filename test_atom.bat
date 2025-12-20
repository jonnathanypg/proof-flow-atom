@echo off
:: Wrapper script to launch the UDF Audit CLI on Windows
:: Automates Virtual Environment setup and dependency installation with smart detection

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

:: 2. Check Virtual Environment
if defined VIRTUAL_ENV (
    echo [INFO] Running inside active virtual environment: %VIRTUAL_ENV%
) else (
    if not exist "venv" (
        echo [INFO] Creating virtual environment...
        python -m venv venv
    )
    call venv\Scripts\activate
)

:: 3. Check Dependencies (Smart Check)
python -c "import requests" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Dependencies already installed.
) else (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt -q
)

:: 4. Run the Menu
echo [INFO] Launching Audit Menu...
python audit_menu.py
pause

