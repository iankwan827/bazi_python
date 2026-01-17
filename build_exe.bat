pip install pyinstaller
python -m PyInstaller --noconsole --onefile --windowed --name="BaziChart" --icon="bazi.ico" --add-data "styles.qss;." run_app.py
pause
