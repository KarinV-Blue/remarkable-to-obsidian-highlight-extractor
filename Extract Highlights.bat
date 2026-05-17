@echo off
title reMarkable Extractor Pipeline

:: Change directory to where your script is located
cd /d "C:\Your\reMarkable\Download"

:: Scan the Python script to find the defined version line
set "script_version=Unknown"
for /f "tokens=2 delims== " %%A in ('findstr "__version__" extract_highlights.py') do (
    set "raw_version=%%~A"
)
:: Clean quotation marks if present
if defined raw_version set "script_version=%raw_version:"=%"

echo --------------------------------------------------
echo Launching Automation Script...
echo Detected Version: v%script_version%
echo --------------------------------------------------
echo.

:: Execute the python script
python extract_highlights.py

echo.
echo --------------------------------------------------
echo Pipeline complete. Press any key to close window...
pause > nul