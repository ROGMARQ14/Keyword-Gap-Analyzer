@echo off
echo Starting Keyword Gap Analyzer...
echo.

:: Check if virtual environment exists
if exist "venv\Scripts\activate" (
    call venv\Scripts\activate
) else (
    echo Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)

:: Run the application
streamlit run app.py --server.port=8501 --server.address=0.0.0.0

pause
