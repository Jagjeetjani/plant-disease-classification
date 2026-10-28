@echo off
title Plant Disease Classification - AI Application Lab
cd /d "%~dp0"

echo ======================================================================
echo         PLANT DISEASE CLASSIFICATION AND BOTANICAL PATHOLOGY
echo                AI Application Lab - Chandigarh University
echo ======================================================================
echo.

REM 1. Detect Python
set "PYTHON_EXE="

REM Try py -3.10
py -3.10 --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_EXE=py -3.10"
    goto :PYTHON_FOUND
)

REM Try py -3
py -3 --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_EXE=py -3"
    goto :PYTHON_FOUND
)

REM Try python
python --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_EXE=python"
    goto :PYTHON_FOUND
)

REM Common standard install locations
if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    goto :PYTHON_FOUND
)

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    goto :PYTHON_FOUND
)

if exist "%ProgramFiles%\Python310\python.exe" (
    set "PYTHON_EXE=%ProgramFiles%\Python310\python.exe"
    goto :PYTHON_FOUND
)

if exist "%ProgramFiles%\Python311\python.exe" (
    set "PYTHON_EXE=%ProgramFiles%\Python311\python.exe"
    goto :PYTHON_FOUND
)

:PYTHON_NOT_FOUND
echo [ERROR] Python was not found on your computer.
echo Please install Python 3.10 or higher from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:PYTHON_FOUND
echo Found Python: %PYTHON_EXE%
%PYTHON_EXE% --version
echo.

REM 2. Check if dependencies are installed
%PYTHON_EXE% -c "import streamlit, tensorflow, PIL, cv2, fpdf, pptx" >nul 2>&1
if not errorlevel 1 (
    echo All dependencies are verified!
    goto :CHECK_MODELS
)

echo [Step 1 of 3] Installing required packages from requirements.txt...
%PYTHON_EXE% -m pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some dependencies reported warnings. Continuing...
)

:CHECK_MODELS
REM 3. Verify if models are trained
if exist "models\mobilenetv2_model.keras" goto :DETECT_PORT

echo.
echo [Step 2 of 3] Training ML classification models...
%PYTHON_EXE% model.py
if errorlevel 1 (
    echo [ERROR] Model training failed.
    pause
    exit /b 1
)

:DETECT_PORT
REM 4. Detect an available free port for Streamlit
set "APP_PORT=8501"
netstat -ano | findstr /R /C:":8501 " >nul 2>&1
if errorlevel 1 goto :LAUNCH_APP

echo [INFO] Port 8501 is currently occupied by another active project.
set "APP_PORT=8502"
netstat -ano | findstr /R /C:":8502 " >nul 2>&1
if errorlevel 1 goto :LAUNCH_APP

set "APP_PORT=8503"
netstat -ano | findstr /R /C:":8503 " >nul 2>&1
if errorlevel 1 goto :LAUNCH_APP

set "APP_PORT=8504"
netstat -ano | findstr /R /C:":8504 " >nul 2>&1
if errorlevel 1 goto :LAUNCH_APP

set "APP_PORT=8505"

:LAUNCH_APP
if not exist "%USERPROFILE%\.streamlit" mkdir "%USERPROFILE%\.streamlit" >nul 2>&1
if not exist "%USERPROFILE%\.streamlit\credentials.toml" (
    echo [general]> "%USERPROFILE%\.streamlit\credentials.toml"
    echo email = "">> "%USERPROFILE%\.streamlit\credentials.toml"
)

echo.
echo ======================================================================
echo  [Step 3 of 3] Launching web application in your browser...
echo  App URL: http://localhost:%APP_PORT%
echo  Active Port: %APP_PORT%
echo  NOTE: Keep this terminal window open while using the application.
echo ======================================================================
echo.

%PYTHON_EXE% -m streamlit run app.py --server.port %APP_PORT% --browser.gatherUsageStats false

echo.
echo Application stopped.
pause
