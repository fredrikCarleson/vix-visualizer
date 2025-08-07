@echo off
echo Building VIX Visualizer executable...
echo.

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable...
pyinstaller --onefile --windowed --name "VIXVisualizer" main.py

echo.
echo Build complete! Check the dist folder for VIXVisualizer.exe
pause 