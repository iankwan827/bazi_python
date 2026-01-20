from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QComboBox, QFrame, QCheckBox, QMessageBox, 
                               QStackedWidget, QGridLayout, QSpinBox, QListWidget, QDialog)
import json
import os
from PySide6.QtCore import Qt
from bazi_logic import calculate_bazi, GAN, ZHI
from bazi_reverse import find_date_from_bazi
from modern_date_picker import DateSelectionDialog
import datetime
from lunar_python import Lunar, Solar

class InputPage(QWidget):
    def __init__(self, on_calculate_cb):
        super().__init__()
        self.on_calculate_cb = on_calculate_cb
        self.current_dt = datetime.datetime(1990, 1, 1, 12, 0)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        # Card Container
        card = QFrame()
        card.setObjectName("ChartCard")
        card.setFixedSize(450, 600) # Increased height for manual input
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(15)
        
        # Title
        title = QLabel("八字排盘")
        title.setObjectName("HeaderTitle")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        
        # Mode Toggle
        mode_layout = QHBoxLayout()
        lbl_mode = QLabel("输入模式")
        lbl_mode.setStyleSheet("color: #aaa; font-weight: bold; font-size: 14px;")
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["日期排盘", "八字反推"])
        self.mode_combo.setFixedHeight(35)
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        
        mode_layout.addWidget(lbl_mode)
        mode_layout.addWidget(self.mode_combo)
        card_layout.addLayout(mode_layout)
        
        # Stacked Widget for Content
        self.stack = QStackedWidget()
        
        # --- Page 1: Date Input ---
        page_date = QWidget()
        page_date_layout = QVBoxLayout(page_date)
        page_date_layout.setContentsMargins(0, 0, 0, 0)
        page_date_layout.setSpacing(15)
        
        # Calendar Type
        type_layout = QHBoxLayout()
        lbl_type = QLabel("历法类型")
        lbl_type.setStyleSheet("color: #aaa; font-weight: bold; font-size: 14px;")
        
        self.cal_type = QComboBox()
        self.cal_type.addItems(["公历 (Solar)", "农历 (Lunar)"])
        self.cal_type.setFixedHeight(35)
        self.cal_type.currentIndexChanged.connect(self.on_type_changed)
        
        # Leap Month Checkbox (Initial Hidden)
        self.chk_leap = QCheckBox("闰月")
        self.chk_leap.setStyleSheet("color: #d35400; font-weight: bold;")
        self.chk_leap.hide()
        
        type_layout.addWidget(lbl_type)
        type_layout.addWidget(self.cal_type)
        type_layout.addWidget(self.chk_leap)
        page_date_layout.addLayout(type_layout)
        
        # Date Button
        self.lbl_date_title = QLabel("出生时间 (公历)")
        self.lbl_date_title.setStyleSheet("color: #aaa; font-weight: bold; font-size: 14px;")
        page_date_layout.addWidget(self.lbl_date_title)
        
        self.btn_date = QPushButton()
        self.btn_date.setFixedHeight(50)
        self.btn_date.setStyleSheet("""
            QPushButton {
                background-color: #252525;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
                font-size: 18px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                border: 1px solid #d35400;
                background-color: #2a2a2a;
            }
        """)
        self.update_date_label()
        self.btn_date.clicked.connect(self.open_date_dialog)
        page_date_layout.addWidget(self.btn_date)
        
        page_date_layout.addStretch()
        self.stack.addWidget(page_date)
        
        # --- Page 2: Manual Input ---
        page_manual = QWidget()
        manual_layout = QVBoxLayout(page_manual)
        manual_layout.setContentsMargins(0, 0, 0, 0)
        manual_layout.setSpacing(10)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        # Headers
        grid.addWidget(QLabel("天干"), 0, 1)
        grid.addWidget(QLabel("地支"), 0, 2)
        
        self.gan_combos = []
        self.zhi_combos = []
        labels = ["年柱", "月柱", "日柱", "时柱"]
        
        for i, lbl_txt in enumerate(labels):
            lbl = QLabel(lbl_txt)
            lbl.setStyleSheet("color: #aaa; font-weight: bold;")
            grid.addWidget(lbl, i+1, 0)
            
            cb_gan = QComboBox()
            cb_gan.addItems(GAN)
            cb_gan.setFixedHeight(35)
            
            cb_zhi = QComboBox()
            cb_zhi.addItems(ZHI)
            cb_zhi.setFixedHeight(35)
            
            self.gan_combos.append(cb_gan)
            self.zhi_combos.append(cb_zhi)
            
            grid.addWidget(cb_gan, i+1, 1)
            grid.addWidget(cb_zhi, i+1, 2)
            
        manual_layout.addLayout(grid)
        
        # Reference Year Removed as per user request
        # Default search range will be centered on 2000

        
        manual_layout.addStretch()
        self.stack.addWidget(page_manual)
        
        # Add Stack to Card
        card_layout.addWidget(self.stack)
        
        # Gender (Common)
        lbl_gender = QLabel("性别")
        lbl_gender.setStyleSheet("color: #aaa; font-weight: bold; font-size: 14px;")
        card_layout.addWidget(lbl_gender)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["男", "女"])
        self.gender_combo.setFixedHeight(45)
        self.gender_combo.setStyleSheet("""
             QComboBox {
                padding-left: 15px;
                font-size: 16px;
             }
        """)
        card_layout.addWidget(self.gender_combo)
        
        # Button Layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_load = QPushButton("读取记录")
        self.btn_load.setMinimumHeight(50)
        self.btn_load.clicked.connect(self.load_chart)
        self.btn_load.setStyleSheet("""
             QPushButton {
                background-color: #333;
                color: #ccc;
                border: 1px solid #555;
                border-radius: 4px;
                font-size: 16px;
             }
             QPushButton:hover {
                background-color: #444;
                border-color: #aaa;
             }
        """)
        
        btn_calc = QPushButton("开始排盘")
        btn_calc.setObjectName("PrimaryBtn")
        btn_calc.setMinimumHeight(50)
        btn_calc.clicked.connect(self.run_calculation)
        
        btn_layout.addWidget(self.btn_load, 1)
        btn_layout.addWidget(btn_calc, 2)
        card_layout.addLayout(btn_layout)
        
        layout.addWidget(card)

    def on_mode_changed(self, idx):
        self.stack.setCurrentIndex(idx)

    def on_type_changed(self, idx):
        is_lunar = (idx == 1)
        self.lbl_date_title.setText("出生时间 (农历)" if is_lunar else "出生时间 (公历)")
        if is_lunar:
            self.chk_leap.show()
        else:
            self.chk_leap.hide()
            self.chk_leap.setChecked(False)

    def update_date_label(self):
        # Format: 1990-01-01 12:00
        txt = self.current_dt.strftime("%Y-%m-%d  %H:%M")
        self.btn_date.setText(txt)
        
    def load_chart(self):
        file_path = "saved_charts.json"
        if not os.path.exists(file_path):
            QMessageBox.information(self, "提示", "暂无保存的记录")
            return
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data_list = json.load(f)
        except:
             QMessageBox.warning(self, "错误", "读取记录失败")
             return

        if not data_list:
            QMessageBox.information(self, "提示", "记录为空")
            return
            
        # Dialog
        dlg = QDialog(self)
        dlg.setWindowTitle("选择存档")
        dlg.setFixedSize(400, 500)
        layout = QVBoxLayout(dlg)
        
        list_widget = QListWidget()
        for idx, item in enumerate(reversed(data_list)): # Show newest first
            name = item.get('name', '无名')
            date = item.get('solarDate', '').split(' ')[0] # just date
            gender = item.get('gender', '')
            saved_at = item.get('savedAt', '')
            list_widget.addItem(f"{name} ({gender}) - {date}\n保存于: {saved_at}")
            
        list_widget.setStyleSheet("font-size: 16px; padding: 5px;")
        layout.addWidget(list_widget)
        
        def on_select():
            sel_items = list_widget.selectedIndexes()
            if not sel_items: return
            # Reverted list, so index map back
            real_idx = len(data_list) - 1 - sel_items[0].row()
            record = data_list[real_idx]
            self.restore_record(record)
            dlg.accept()
            
        list_widget.doubleClicked.connect(on_select)
        
        btn_layout = QHBoxLayout()
        btn_del = QPushButton("删除记录")
        btn_del.setStyleSheet("background-color: #c0392b;") # Redish
        
        def on_delete():
            sel_items = list_widget.selectedIndexes()
            if not sel_items: return
            
            confirm = QMessageBox.question(dlg, "确认删除", "确定要删除这条记录吗？", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                row = sel_items[0].row()
                real_idx = len(data_list) - 1 - row
                data_list.pop(real_idx)
                
                # Update File
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(data_list, f, ensure_ascii=False, indent=4)
                    list_widget.takeItem(row)
                except Exception as e:
                    QMessageBox.warning(dlg, "错误", f"删除失败: {str(e)}")

        btn_del.clicked.connect(on_delete)
        
        btn_ok = QPushButton("读取")
        btn_ok.clicked.connect(on_select)
        
        btn_layout.addWidget(btn_del)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)
        
        dlg.exec()

    def restore_record(self, record):
        # 1. Parse Date String "YYYY-MM-DD HH:MM:SS (公历)" to datetime
        # Assuming saved format is consistent from chart_view
        s_date = record['solarDate'] 
        # Extract YMDH
        try:
            # Example: "2024-01-01 12:00:00 (公历)" or just "2024-01-01 12:00:00"
            s_date = s_date.split('(')[0].strip()
            dt = datetime.datetime.strptime(s_date, "%Y-%m-%d %H:%M:%S")
            
            self.current_dt = dt
            self.update_date_label()
            
            # Set Gender
            gender_txt = record.get('gender', '男')
            # Handle both '男'/'女' and 'M'/'F'
            is_male = str(gender_txt).upper() in ['男', 'M', 'MALE']
            idx = 0 if is_male else 1
            self.gender_combo.setCurrentIndex(idx)
            
            # Switch to Date Mode
            self.mode_combo.setCurrentIndex(0)
            self.cal_type.setCurrentIndex(0) # Logic assumes saved as Solar. User sees "公历" in saved JSON.
            
            # Auto Run
            self.run_calculation()
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"解析日期失败: {s_date}\n{str(e)}")


    def open_date_dialog(self):
        dlg = DateSelectionDialog(self.current_dt, self)
        if dlg.exec():
            self.current_dt = dlg.get_date_time()
            self.update_date_label()
        
    def run_calculation(self):
        gender = 'M' if self.gender_combo.currentText() == '男' else 'F'
        
        if self.mode_combo.currentIndex() == 1: # Manual Reverse
            # Gather Pillars
            y_g = self.gan_combos[0].currentText()
            y_z = self.zhi_combos[0].currentText()
            m_g = self.gan_combos[1].currentText()
            m_z = self.zhi_combos[1].currentText()
            d_g = self.gan_combos[2].currentText()
            d_z = self.zhi_combos[2].currentText()
            t_g = self.gan_combos[3].currentText()
            t_z = self.zhi_combos[3].currentText()
            ref_year = 2000 # Default center for search
            
            results = find_date_from_bazi(y_g, y_z, m_g, m_z, d_g, d_z, t_g, t_z, ref_year)
            
            if not results:
                QMessageBox.warning(self, "反推失败", f"在 {ref_year} 年前后未找到匹配的八字日期。\n请检查干支输入是否合法（如是否符合六十甲子规律）。")
                return
            
            # Handle multiple results
            solar_selected = None
            if len(results) == 1:
                solar_selected = results[0]
            else:
                # Format options for user to choose
                options = []
                for sol in results:
                    # e.g. "2002-02-06 (周三) 22:00"
                    # Add GanZhi context if needed? Already known.
                    # Just show Date.
                    s = f"{sol.getYear()}-{sol.getMonth():02d}-{sol.getDay():02d} {sol.getHour():02d}:00"
                    options.append(s)
                
                from PySide6.QtWidgets import QInputDialog
                item, ok = QInputDialog.getItem(self, "选择日期", 
                                              f"找到 {len(results)} 个匹配日期，请选择：", 
                                              options, 0, False)
                if ok and item:
                    idx = options.index(item)
                    solar_selected = results[idx]
                else:
                    return # Cancelled

            # Found!
            final_dt = datetime.datetime(solar_selected.getYear(), solar_selected.getMonth(), solar_selected.getDay(), 
                                         solar_selected.getHour(), solar_selected.getMinute())
            
        else:
            # Date Mode
            final_dt = self.current_dt
            
            # Lunar Conversion Logic
            if self.cal_type.currentIndex() == 1: # Lunar Selected
                try:
                    y = self.current_dt.year
                    m = self.current_dt.month
                    d = self.current_dt.day
                    h = self.current_dt.hour
                    mi = self.current_dt.minute
                    
                    # Base Lunar Date (defaults to non-leap)
                    lunar = Lunar.fromYmdHms(y, m, d, h, mi, 0)
                    
                    # Handle Leap Month
                    if self.chk_leap.isChecked():
                        leap_month = lunar.getYearLeapMonth()
                        if leap_month == 0:
                             QMessageBox.warning(self, "农历错误", f"{y}年没有闰月！")
                             return
                        if leap_month != abs(lunar.getMonth()):
                             QMessageBox.warning(self, "农历错误", f"{y}年的闰月是{leap_month}月，不是{m}月！")
                             return
                        
                        # Move to the leap month (Add days of normal month)
                        # Note: next() returns a new Lunar object
                        lunar = lunar.next(lunar.getDayCount())
                    
                    # Convert to Solar
                    solar = lunar.getSolar()
                    final_dt = datetime.datetime(solar.getYear(), solar.getMonth(), solar.getDay(), 
                                               solar.getHour(), solar.getMinute())
                                               
                except Exception as e:
                    QMessageBox.warning(self, "输入错误", f"农历转换失败: {str(e)}")
                    return
        
        # Call Logic
        result = calculate_bazi(final_dt, gender)
        
        # Callback to Main Window
        if self.on_calculate_cb:
            self.on_calculate_cb(result)
