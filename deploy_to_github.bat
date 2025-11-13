@echo off
echo ========================================
echo   Deploy Timetable Generator to GitHub
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Step 1: Initializing Git repository...
git init

echo.
echo Step 2: Adding files to Git...
git add .

echo.
echo Step 3: Creating initial commit...
git commit -m "Initial commit - Timetable Generator Streamlit App"

echo.
echo ========================================
echo   Next Steps:
echo ========================================
echo.
echo 1. Create a new repository on GitHub:
echo    https://github.com/new
echo.
echo 2. Name it: timetable-generator
echo.
echo 3. Run these commands (replace YOUR_USERNAME):
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/timetable-generator.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Deploy on Streamlit Cloud:
echo    https://share.streamlit.io/
echo.
echo ========================================
pause
