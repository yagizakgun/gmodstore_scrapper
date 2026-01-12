@echo off
echo ================================================
echo GModStore Job Market Discord Scraper
echo ================================================
echo.

REM Virtual environment'i aktifleştir ve uygulamayı başlat
call venv\Scripts\activate.bat
python main.py

pause
