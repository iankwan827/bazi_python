from PySide6.QtWidgets import QApplication
import sys
import datetime
from modern_date_picker import DateSelectionDialog

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

print("--- Launching Dialog with 1987-01-01 ---")
dt = datetime.datetime(1987, 1, 1, 13, 0)
dlg = DateSelectionDialog(dt)
# We use QTimer to close it automatically after a few seconds so the script finishes and we see logs
from PySide6.QtCore import QTimer
QTimer.singleShot(2000, dlg.accept) # Close after 2s

dlg.exec()
print("Dialog Closed")
