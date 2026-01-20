import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QStackedWidget, QPushButton, QLabel, QFrame)
from PySide6.QtCore import Qt, QFile, QTextStream

from input_page import InputPage
from chart_view import ChartPage
from detailed_view import DetailedAnalysisPage
from judgment_formulas_page import JudgmentFormulasPage

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
        
        labels = ["基本信息", "基本排盘", "专业细盘", "断事口诀"]
        
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
        self.prof_page = DetailedAnalysisPage()
        
        # Connect Active Luck Update
        self.chart_page.activePillarsChanged.connect(self.prof_page.set_active_luck)
        
        # Judgment Formulas Page
        self.formulas_page = JudgmentFormulasPage()
        
        self.stack.addWidget(self.input_page) # 0
        self.stack.addWidget(self.chart_page) # 1
        self.stack.addWidget(self.prof_page)  # 2
        self.stack.addWidget(self.formulas_page) # 3
        
    def switch_tab(self, idx):
        self.stack.setCurrentIndex(idx)
        
    def on_calculate(self, data):
        # Calculate Logic
        self.chart_page.render_data(data)
        self.prof_page.render_data(data)
        self.formulas_page.render_data(data)
        
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
