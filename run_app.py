from main_window import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream
import sys

# High DPI Setup
import os
os.environ["QT_FONT_DPI"] = "96"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Load Styles
    style_path = os.path.join(os.path.dirname(__file__), "styles.qss")
    file = QFile(style_path)
    if file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())
        file.close()
    else:
        # Fallback to Dark Theme if QSS missing
        import sys
        print("WARNING: styles.qss not found!")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#121212"))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor("#1e1e1e"))
        palette.setColor(QPalette.AlternateBase, QColor("#121212"))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor("#121212"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
