import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QStackedWidget, QPushButton, QLabel, QFrame)
from PySide6.QtCore import Qt, QFile, QTextStream

from input_page import InputPage
from chart_view import ChartPage

class TopNavBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TopNavBar")
        self.setFixedHeight(50)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignLeft)
        
        self.buttons = []
        self.btn_group = []
        
        labels = ["基本信息", "基本排盘", "专业细盘", "断事笔记"]
        
        for i, text in enumerate(labels):
            btn = QPushButton(text)
            btn.setObjectName("NavBtn")
            btn.setCheckable(True)
            if i == 0: btn.setChecked(True)
            btn.clicked.connect(lambda checked, idx=i: self.on_btn_clicked(idx))
            layout.addWidget(btn)
            self.buttons.append(btn)
            
        self.on_tab_changed = None

    def on_btn_clicked(self, idx):
        # Update UI state
        self.set_active_tab(idx)
        # Emit signal
        if self.on_tab_changed:
            self.on_tab_changed(idx)
            
    def set_active_tab(self, idx):
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == idx)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("智能八字排盘系统")
        self.resize(1200, 850)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        
        # Top Navigation
        self.nav_bar = TopNavBar()
        self.nav_bar.on_tab_changed = self.switch_tab
        main_layout.addWidget(self.nav_bar)
        
        # Stacked Widget for Pages
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        
        # Pages
        self.input_page = InputPage(self.on_calculate)
        self.chart_page = ChartPage(self.on_back)
        
        # Placeholders
        self.prof_page = QLabel("专业细盘 - 开发中")
        self.prof_page.setAlignment(Qt.AlignCenter)
        self.prof_page.setStyleSheet("font-size: 24px; color: #666;")
        
        self.notes_page = QLabel("断事笔记 - 开发中")
        self.notes_page.setAlignment(Qt.AlignCenter)
        self.notes_page.setStyleSheet("font-size: 24px; color: #666;")
        
        self.stack.addWidget(self.input_page) # 0
        self.stack.addWidget(self.chart_page) # 1
        self.stack.addWidget(self.prof_page)  # 2
        self.stack.addWidget(self.notes_page) # 3
        
    def switch_tab(self, idx):
        self.stack.setCurrentIndex(idx)
        
    def on_calculate(self, data):
        # Calculate Logic
        self.chart_page.render_data(data)
        
        # Switch to Chart Tab (Index 1)
        self.stack.setCurrentIndex(1)
        self.nav_bar.set_active_tab(1)
        
    def on_back(self):
        # Switch to Input Tab (Index 0)
        self.stack.setCurrentIndex(0)
        self.nav_bar.set_active_tab(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Load Styles
    file = QFile("styles.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
