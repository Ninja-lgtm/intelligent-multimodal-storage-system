@echo off
echo ================================================
echo  Intelligent Multi-Modal Storage System
echo  Starting Backend Server...
echo ================================================
echo.

cd backend

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask server...
echo.
python app.py

pause
