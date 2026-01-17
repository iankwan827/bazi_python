#!/bin/bash
# Install PyInstaller if not present
pip install pyinstaller

# Build for Linux (Deepin, UOS, Ubuntu, etc.)
# Note: Separator for add-data is ':' on Linux/Mac, ';' on Windows
python3 -m PyInstaller --noconsole --onefile --name="BaziChart" --add-data "styles.qss:." run_app.py

echo "Build complete! Check the 'dist' folder for the executable."
