from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                               QListWidgetItem, QLabel, QFrame, QAbstractItemView, QPushButton, QScroller, QScrollerProperties)
from PySide6.QtCore import Qt, Signal, QSize, QTimer
from PySide6.QtGui import QFont, QColor, QBrush

class WheelColumn(QListWidget):
    itemChangedSignal = Signal(str)

    def __init__(self, items, suffix="", parent=None, width=90):
        super().__init__(parent)
        self.suffix = suffix
        self.raw_items = [str(i) for i in items]
        
        # UI Setup
        self.setFixedWidth(width)
        self.setFixedHeight(180) # Increased height for better view
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("background: transparent; border: none;")
        
        # Scroll Mode
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSelectionMode(QAbstractItemView.NoSelection) 
        self.setFocusPolicy(Qt.NoFocus) 
        
        # Add Padding Items
        for _ in range(5):
             it = QListWidgetItem("")
             it.setSizeHint(QSize(width, 30))
             self.addItem(it)
        
        # Add Real Items
        for t in self.raw_items:
             item = QListWidgetItem(f"{t}{suffix}")
             item.setTextAlignment(Qt.AlignCenter)
             item.setData(Qt.UserRole, t)
             item.setSizeHint(QSize(width, 30))
             self.addItem(item)
             
        # Add Padding Items
        for _ in range(5):
             it = QListWidgetItem("")
             it.setSizeHint(QSize(width, 30))
             self.addItem(it)

        # Kinetic Scrolling
        QScroller.grabGesture(self.viewport(), QScroller.LeftMouseButtonGesture)
        scroller = QScroller.scroller(self.viewport())
        props = scroller.scrollerProperties()
        props.setScrollMetric(QScrollerProperties.DragStartDistance, 0.001)
        props.setScrollMetric(QScrollerProperties.DecelerationFactor, 0.5)
        scroller.setScrollerProperties(props)
        
        # Timer for snapping
        self.snap_timer = QTimer()
        self.snap_timer.setSingleShot(True)
        self.snap_timer.timeout.connect(self.snap_to_grid)
        
        # Events
        self.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.itemClicked.connect(self.on_item_clicked)

    def highlight_item(self, target):
        for i in range(self.count()):
            it = self.item(i)
            font = it.font()
            if it == target:
                font.setBold(True)
                font.setPointSize(14)
                it.setForeground(QBrush(QColor("#d35400")))
            else:
                font.setBold(False)
                font.setPointSize(10)
                it.setForeground(QBrush(QColor("#666666")))
            it.setFont(font)

    def on_scroll(self):
        self.snap_timer.start(100) 
        self.update_styles()

    def update_styles(self):
        center_y = self.height() // 2
        center_item = self.itemAt(self.width()//2, center_y)
        if center_item and center_item.text() != "":
            self.highlight_item(center_item)

    def on_item_clicked(self, item):
        if item.text() != "":
            self.scrollToItem(item, QAbstractItemView.PositionAtCenter)
            self.snap_to_grid() 

    def snap_to_grid(self):
        center_y = self.height() // 2
        center_item = self.itemAt(self.width()//2, center_y)
        
        if center_item:
            if center_item.text() == "":
                row = self.row(center_item)
                if row < 5: 
                    center_item = self.item(5) 
                else: 
                    center_item = self.item(self.count() - 6) 
            
            if center_item:
                val = center_item.data(Qt.UserRole)
                self.scrollToItem(center_item, QAbstractItemView.PositionAtCenter)
                self.highlight_item(center_item)
                
                if val:
                    self.itemChangedSignal.emit(val)
            
    def get_value(self):
        center_item = self.itemAt(self.width()//2, self.height()//2)
        if center_item and center_item.text() != "":
            return center_item.data(Qt.UserRole)
        # Fallback to defaults if scrolling or empty
        return self.raw_items[0]

    def set_value(self, val):
        val_s = str(val)

        for i in range(self.count()):
            it = self.item(i)
            if it.data(Qt.UserRole) == val_s:

                self.scrollToItem(it, QAbstractItemView.PositionAtCenter)
                self.highlight_item(it)
                return


class ModernDatePicker(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(5)
        
        # Years
        years = range(1900, 2100)
        self.year_col = WheelColumn(years, "年", width=120)
        layout.addWidget(self.year_col)
        
        # Months
        months = range(1, 13)
        self.month_col = WheelColumn(months, "月", width=70)
        layout.addWidget(self.month_col)
        
        # Days
        days = range(1, 32)
        self.day_col = WheelColumn(days, "日", width=70)
        layout.addWidget(self.day_col)
        
        # Separator Line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet("color: #444;")
        layout.addWidget(line)

        # Hours
        hours = range(0, 24)
        self.hour_col = WheelColumn(hours, "时", width=70)
        layout.addWidget(self.hour_col)
        
        # Minutes
        minutes = range(0, 60)
        self.minute_col = WheelColumn(minutes, "分", width=70)
        layout.addWidget(self.minute_col)

        # Defaults
        # Removed automatic default to 'now' to prevent conflict with external set_datetime calls
        # The parent (DateSelectionDialog) is responsible for setting the initial time.
        
    def get_date_time(self):
        y = int(self.year_col.get_value() or 1990)
        m = int(self.month_col.get_value() or 1)
        d = int(self.day_col.get_value() or 1)
        h = int(self.hour_col.get_value() or 0)
        mi = int(self.minute_col.get_value() or 0)
        
        # Validation for days (e.g. Feb 30)
        import calendar
        try:
            max_days = calendar.monthrange(y, m)[1]
            if d > max_days: d = max_days
        except:
            pass
            
        import datetime
        return datetime.datetime(y, m, d, h, mi)

    def set_datetime(self, y, m, d, h, mi):
        # Increased delay to 300ms to ensure visual rects are ready
        QTimer.singleShot(300, lambda: self._do_set(y, m, d, h, mi))
        
    def _do_set(self, y, m, d, h, mi):
        self.year_col.set_value(y)
        self.month_col.set_value(m)
        self.day_col.set_value(d)
        self.hour_col.set_value(h)
        self.minute_col.set_value(mi)

from PySide6.QtWidgets import QDialog

class DateSelectionDialog(QDialog):
    def __init__(self, initial_dt=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择出生时间")
        self.setFixedWidth(550)
        self.setStyleSheet("background-color: #252525; color: white; border-radius: 12px;")
        
        # Remove default window frame for custom look? 
        # Or keep system frame but ensure content matches.
        # Let's keep system frame for now but style content.
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #333; border-bottom: 1px solid #3d3d3d; border-top-left-radius: 12px; border-top-right-radius: 12px;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(15, 10, 15, 10)
        
        lbl_title = QLabel("选择出生时间")
        lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #eee; border: none;")
        
        btn_close = QPushButton("×")
        btn_close.setFixedSize(30, 30)
        btn_close.clicked.connect(self.reject)
        btn_close.setStyleSheet("background: transparent; color: #888; font-size: 24px; border: none; font-weight: bold;")
        
        hl.addWidget(lbl_title)
        hl.addStretch()
        hl.addWidget(btn_close)
        
        layout.addWidget(header)
        
        # Wheel Picker
        self.picker = ModernDatePicker()
        self.picker.setStyleSheet("background-color: #252525;")
        
        if initial_dt:
            self.picker.set_datetime(
                initial_dt.year, initial_dt.month, initial_dt.day,
                initial_dt.hour, initial_dt.minute
            )
        else:
            import datetime
            now = datetime.datetime.now()
            self.picker.set_datetime(now.year, now.month, now.day, 12, 0)
        layout.addWidget(self.picker)

        # Footer Buttons
        footer = QFrame()
        footer.setStyleSheet("background-color: #333; border-top: 1px solid #3d3d3d; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;")
        btn_layout = QHBoxLayout(footer)
        btn_layout.setContentsMargins(15, 15, 15, 15)
        btn_layout.setSpacing(15)
        
        btn_cancel = QPushButton("取消")
        btn_cancel.clicked.connect(self.reject)
        btn_cancel.setFixedHeight(45)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #444; 
                color: #bbb; 
                border: none; 
                border-radius: 6px; 
                font-size: 16px; 
                font-weight: bold;
            }
            QPushButton:hover { background-color: #555; }
        """)
        
        btn_conf = QPushButton("确定")
        btn_conf.clicked.connect(self.accept)
        btn_conf.setFixedHeight(45)
        btn_conf.setStyleSheet("""
            QPushButton {
                background-color: #d35400; 
                color: white; 
                border: none; 
                border-radius: 6px; 
                font-size: 16px; 
                font-weight: bold;
            }
            QPushButton:hover { background-color: #e67e22; }
        """)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_conf)
        
        layout.addWidget(footer)
        
    def get_date_time(self):
        return self.picker.get_date_time()
