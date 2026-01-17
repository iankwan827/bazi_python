#!/bin/bash
# Install PyInstaller if not present
pip install pyinstaller

# Build for macOS
# --windowed required for GUI apps on Mac
python3 -m PyInstaller --noconsole --onefile --windowed --name="BaziChart" --add-data "styles.qss:." run_app.py

# Note: On macOS, --onefile combined with --windowed often creates a .app bundle inside dist/
# If you strictly want a command line binary, remove --windowed, but for GUI apps .app is standard.
echo "Build complete! Check the 'dist' folder."
