from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGridLayout, QScrollArea, QFrame, QSizePolicy,
                             QTableView, QHeaderView, QAbstractItemView, QStyledItemDelegate, QPushButton,
                             QInputDialog, QMessageBox)
from PySide6.QtCore import Qt, Signal, QTimer, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QPalette, QPainter, QPen, QTextDocument, QFont
from bazi_logic import get_ten_god, get_shen_sha, get_kong_wang, get_color, calculate_bazi, get_dynamic_interactions
import datetime
from lunar_python import Solar
import json
import os

class LiuNianModel(QAbstractTableModel):
    def __init__(self, dayun_list):
        super().__init__()
        self.dayun_list = dayun_list[:8]
        self.ROWS = 10

    def rowCount(self, parent=QModelIndex()):
        return self.ROWS

    def columnCount(self, parent=QModelIndex()):
        return len(self.dayun_list)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid(): return None
        if role == Qt.UserRole:
            col = index.column()
            row = index.row()
            dy = self.dayun_list[col]
            ln_list = dy.get('liuNian', [])
            if row < len(ln_list):
                return ln_list[row]
            return None # Placeholder
        return None

class LiuNianDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, color_func=None):
        super().__init__(parent)
        self.color_func = color_func
        self.line_color = QColor("#383838")
        self.active_border = QColor("#d35400")
        self.active_bg = QColor("#3e2723")
        self.normal_bg = QColor("#252525")

    def paint(self, painter, option, index):
        painter.save()
        data = index.data(Qt.UserRole)
        rect = option.rect
        
        is_current = False
        is_current = False
        if data:
            now = datetime.datetime.now()
            # Robust Li Chun Logic
            gregorian_year = now.year
            bazi_year = gregorian_year
            try:
                s = Solar.fromYmd(gregorian_year, 2, 4)
                l = s.getLunar()
                jq = l.getJieQiTable()
                if '立春' in jq:
                    lc = jq['立春']
                    lc_dt = datetime.datetime(lc.getYear(), lc.getMonth(), lc.getDay(), 
                                              lc.getHour(), lc.getMinute(), lc.getSecond())
                    if now < lc_dt:
                        bazi_year -= 1
                else:
                    if now.month < 2 or (now.month == 2 and now.day < 4):
                        bazi_year -= 1
            except:
                 if now.month < 2 or (now.month == 2 and now.day < 4):
                    bazi_year -= 1

            is_current = (data['year'] == bazi_year)
            
        # 1. Background
        bg = self.active_bg if is_current else self.normal_bg
        painter.fillRect(rect, bg)
        
        # 2. Borders (Table Grid Lines)
        # Draw Right and Bottom for every cell to match "Grid" look
        pen = QPen(self.line_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawLine(rect.topRight(), rect.bottomRight())
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        
        # 3. Highlight Border (Overrides)
        if is_current:
            pen_hi = QPen(self.active_border)
            pen_hi.setWidth(2)
            painter.setPen(pen_hi)
            # Draw inside boundary
            r = rect.adjusted(1,1,-1,-1)
            painter.drawRect(r)

        # 4. Content
        if data:
            # Use QTextDocument for Rich Text (Colors)
            doc = QTextDocument()
            doc.setDefaultStyleSheet("p { margin: 0; }")
            
            gz = data['ganZhi']
            g = gz[0] if len(gz)>0 else ""
            z = gz[1] if len(gz)>1 else ""
            
            c1 = self.color_func(g) if self.color_func else "#eee"
            c2 = self.color_func(z) if self.color_func else "#eee"
            
            html = f"""
            <div style='text-align: center;'>
                <div style='font-size: 20px; font-weight: bold; font-family: KaiTi; margin-bottom: 2px;'>
                    <span style='color:{c1}'>{g}</span><span style='color:{c2}'>{z}</span>
                </div>
                <div style='color: #888; font-size: 13px;'>{data['year']}({data['age']})</div>
            </div>
            """
            doc.setHtml(html)
            doc.setTextWidth(rect.width())
            
            # Center vertically
            height = doc.size().height()
            y_off = (rect.height() - height) / 2
            
            painter.translate(rect.x(), rect.y() + y_off)
            doc.drawContents(painter)
            
        painter.restore()

# ... [Inside ChartView] ...



class ChartPage(QWidget):
    # Signal emitted when active luck/year changes
    # Args: da_yun_dict, liu_nian_dict
    activePillarsChanged = Signal(dict, dict)

    def __init__(self, on_back_cb):
        super().__init__()
        self.on_back_cb = on_back_cb
        self.current_data = None
        self.selected_dayun_idx = -1
        self.init_ui()
        
    def save_chart(self):
        if not self.current_data:
            return

        text, ok = QInputDialog.getText(self, "保存命盘", "请输入命主姓名:")
        if ok and text:
            name = text.strip()
            if not name:
                return

            record = {
                "name": name,
                "solarDate": self.current_data['solarDate'], # Contains format "YYYY-MM-DD HH:00:00 (公历)"
                "gender": self.current_data['gender'],
                "savedAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            file_path = "saved_charts.json"
            data_list = []
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data_list = json.load(f)
                except:
                    pass

            # Check for existing record with same name
            existing_idx = -1
            for i, item in enumerate(data_list):
                if item.get('name') == name:
                    existing_idx = i
                    break
            
            if existing_idx != -1:
                confirm = QMessageBox.question(self, "覆盖确认", f"已存在名为“{name}”的存档。\n是否覆盖？", QMessageBox.Yes | QMessageBox.No)
                if confirm != QMessageBox.Yes:
                    return
                # Update existing
                data_list[existing_idx] = record
            else:
                # Add new
                data_list.append(record)

            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data_list, f, ensure_ascii=False, indent=4)
                QMessageBox.information(self, "成功", "命盘保存成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")

    def init_ui(self):
        # Scrollable Main View
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        
        # Header
        self.header = QWidget()
        self.header_layout = QHBoxLayout(self.header)
        self.lbl_date = QLabel("")
        self.btn_back = QPushButton("重新排盘")
        self.btn_back.clicked.connect(self.go_back)
        
        self.header_layout.addWidget(self.lbl_date)
        self.header_layout.addStretch()
        
        # Save Button (Replaces "Re-calculate" as per user request)
        self.btn_save = QPushButton("保存命盘")
        self.btn_save.clicked.connect(self.save_chart)
        self.header_layout.addWidget(self.btn_save)
        
        main_layout.addWidget(self.header)
        
        # Content Scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(20)
        self.content_layout.setContentsMargins(20, 10, 20, 20)
        
        self.scroll.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll)
        
        # 1. Top Section (Merged Grid)
        self.top_section = QFrame()
        # No ID to clean borders
        self.top_layout = QVBoxLayout(self.top_section)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.addWidget(self.top_section)
        
        # 2. Middle Section (Details)
        self.mid_section = QFrame()
        self.mid_section.setObjectName("ChartCard")
        self.mid_layout = QVBoxLayout(self.mid_section)
        self.content_layout.addWidget(self.mid_section)
        
        # 3. Bottom Section (Da Yun List)
        self.bot_section = QFrame()
        # self.bot_section.setObjectName("ChartCard") # REMOVE CARD STYLE
        self.bot_section.setStyleSheet("background: transparent; border: none;") # Transparent
        self.bot_layout = QVBoxLayout(self.bot_section)
        self.content_layout.addWidget(self.bot_section)
        
        # 4. Liu Nian List (Hidden by default - though now shown in main chart, keep for extra info?)
        # User image implies Liu Nian IS in the chart. We can keep this for clicking on other Da Yuns.
        self.ln_section = QFrame()
        self.ln_section.setObjectName("ChartCard")
        self.ln_layout = QVBoxLayout(self.ln_section)
        self.content_layout.addWidget(self.ln_section)
        self.ln_section.hide()

    def go_back(self):
        if self.on_back_cb:
            self.on_back_cb()

    def get_current_bazi_year(self):
        """
        Robustly determine current Bazi year using Li Chun.
        """
        import datetime
        now = datetime.datetime.now()
        gregorian_year = now.year
        bazi_year = gregorian_year
        try:
            s = Solar.fromYmd(gregorian_year, 2, 4)
            l = s.getLunar()
            jq = l.getJieQiTable()
            if '立春' in jq:
                lc = jq['立春']
                lc_dt = datetime.datetime(lc.getYear(), lc.getMonth(), lc.getDay(), 
                                          lc.getHour(), lc.getMinute(), lc.getSecond())
                if now < lc_dt:
                    bazi_year -= 1
            else:
                 if now.month < 2 or (now.month == 2 and now.day < 4):
                    bazi_year -= 1
        except:
             if now.month < 2 or (now.month == 2 and now.day < 4):
                bazi_year -= 1
        return bazi_year

    def render_data(self, data):
        # Store for refreshes
        self.current_data = data
        
        # Update Header
        self.lbl_date.setText(f"{data['solarDate']}  |  {data['lunarDate']}")
        self.lbl_date.setObjectName("HeaderTitle")
        
        # Clear previous mid/bot layouts (Top is cleared in render_main_pillars)
        self.clear_layout(self.mid_layout)
        self.clear_layout(self.bot_layout)
        
        # --- Prepare Initial Data ---
        da_yun_list = data['daYunList']
        
        # Backend provided current
        current_dy = data.get('currentDaYun')
        
        # Fallback
        if not current_dy:
             current_age = self.calculate_age(data['solarDate'])
             active_idx = self.find_active_dayun(da_yun_list, current_age)
             current_dy = da_yun_list[active_idx] if active_idx != -1 else None
        
        # Robust Li Chun Logic for Current Liu Nian Selection
        bazi_year = self.get_current_bazi_year()
                
        current_ln = None
        if current_dy:
             current_ln = next((ln for ln in current_dy['liuNian'] if ln['year'] == bazi_year), None)
        if not current_ln:
             current_ln = self.get_fallback_liunian(bazi_year)
             
        # Render Pillars (Top)
        self.render_main_pillars(current_dy, current_ln)
        
        # Render Interactions (Middle)
        # Render Interactions (Middle)
        dynamic_cols = None
        if current_dy and current_ln:
            norm_dy = self.normalize_luck(current_dy)
            norm_ln = self.normalize_luck(current_ln)
            dynamic_cols = [norm_dy, norm_ln]
            
        self.render_interactions(data['interactions'], dynamic_cols)
        
        # Render Matrix (Bottom)
        self.render_dayun_section(da_yun_list)
        

    def render_interactions(self, original_inter, dynamic_pillars=None):
        self.clear_layout(self.mid_layout)
        # dynamic_pillars: list of [dy, ln] objects (normalized)
        
        container = QWidget()
        main_h = QHBoxLayout(container)
        main_h.setContentsMargins(0,0,0,0)
        main_h.setSpacing(20)
        
        # --- Left: Original ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0,0,0,0)
        
        lbl_orig = QLabel("原局关系")
        lbl_orig.setObjectName("SectionTitle")
        left_layout.addWidget(lbl_orig)
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("天干:"))
        row1.addWidget(QLabel(" ".join(original_inter['stems']) if original_inter['stems'] else "无"))
        row1.addStretch()
        left_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("地支:"))
        lbl_zhi = QLabel(" ".join(original_inter['branches']) if original_inter['branches'] else "无")
        lbl_zhi.setWordWrap(True) 
        row2.addWidget(lbl_zhi)
        row2.addStretch()
        left_layout.addLayout(row2)
        
        main_h.addWidget(left_widget, 1)
        
        # --- Vertical Line ---
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #d35400; width: 2px;") 
        main_h.addWidget(line)
        
        # --- Right: Dynamic ---
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0,0,0,0)
        
        dy_text = "请选择大运/流年"
        if dynamic_pillars:
            # Calculate Dynamic Interactions
            # We need to construct the full 6-pillar list to pass to logic
            # data['pillars'] has 4. dynamic_pillars has 2.
            # But get_dynamic_interactions expects simpler dicts or objects?
            # It expects objects with 'gan', 'zhi'.
            # Our normalized pillars have 'gan', 'zhi'.
            # Original pillars in self.current_data['pillars'] also have 'gan', 'zhi'.
            
            all_pillars = self.current_data['pillars'] + dynamic_pillars
            dyn_res = get_dynamic_interactions(all_pillars, [4, 5])
            
            stems_str = " ".join(dyn_res['stems']) if dyn_res['stems'] else "无"
            branches_str = " ".join(dyn_res['branches']) if dyn_res['branches'] else "无"
            
            # Label
            dy_gan_zhi = f"{dynamic_pillars[0]['gan']}{dynamic_pillars[0]['zhi']}"
            ln_gan_zhi = f"{dynamic_pillars[1]['gan']}{dynamic_pillars[1]['zhi']}"
            
            lbl_dyn = QLabel(f"大运({dy_gan_zhi}) 流年({ln_gan_zhi}) 关系")
            lbl_dyn.setObjectName("SectionTitle") # Re-use style or new one?
            lbl_dyn.setStyleSheet("color: #d35400; font-weight: bold;")
            right_layout.addWidget(lbl_dyn)
            
            r1 = QHBoxLayout()
            r1.addWidget(QLabel("天干:"))
            r1.addWidget(QLabel(stems_str))
            r1.addStretch()
            right_layout.addLayout(r1)
            
            r2 = QHBoxLayout()
            r2.addWidget(QLabel("地支:"))
            lbl_d_zhi = QLabel(branches_str)
            lbl_d_zhi.setWordWrap(True)
            r2.addWidget(lbl_d_zhi)
            r2.addStretch()
            right_layout.addLayout(r2)
        else:
            right_layout.addWidget(QLabel("无动态信息"))
            
        main_h.addWidget(right_widget, 1)
        
        self.mid_layout.addWidget(container)

    def normalize_luck(self, obj):
        if not obj:
            return {'gan': '?', 'zhi': '?', 'ganColor': '#888', 'zhiColor': '#888', 'tenGod': '', 'hidden': [], 'naYin': '', 'shenSha': [], 'kongWang': ''}
        
        gz = obj.get('ganZhi', '  ')
        return {
            'gan': gz[0] if len(gz)>0 else '',
            'zhi': gz[1] if len(gz)>1 else '',
            'ganColor': obj.get('ganColor', '#ccc'),
            'zhiColor': obj.get('zhiColor', '#ccc'),
            'tenGod': obj.get('tenGod', ''), 
            'hidden': obj.get('hidden', []),
            'naYin': obj.get('naYin', ''),
            'shenSha': obj.get('shenSha', []),
            'kongWang': obj.get('kongWang', '')
        }

    def render_main_pillars(self, dy_obj, ln_obj):
        self.clear_layout(self.top_layout)
        
        col_dy = self.normalize_luck(dy_obj)
        col_ln = self.normalize_luck(ln_obj)
        
        # The 6 columns
        cols_data = self.current_data['pillars'] + [col_dy, col_ln]
        col_headers = ["年柱", "月柱", "日柱", "时柱", "大运", "流年"]
        
        chart_container = QWidget()
        chart_container.setObjectName("ChartGrid")
        chart_container.setStyleSheet("#ChartGrid { border-top: 1px solid #383838; border-left: 1px solid #383838; }")
        
        chart_v = QVBoxLayout(chart_container)
        chart_v.setSpacing(0)
        chart_v.setContentsMargins(0,0,0,0)
        
        # --- Stripe Helper ---
        def add_stripe(title, cell_widgets, bg_color="transparent", height=None, is_fixed=True):
            row_frame = QFrame()
            row_frame.setStyleSheet(f"background-color: {bg_color}; border-radius: 0px;")
            if height:
                if is_fixed:
                    row_frame.setFixedHeight(height)
                else:
                    row_frame.setMinimumHeight(height)
                    row_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            
            rl = QHBoxLayout(row_frame)
            rl.setContentsMargins(0,0,0,0)
            rl.setSpacing(0)
            
            # Helper: Cell
            def make_cell(widget, is_header=False):
                cell = QFrame()
                cell.setStyleSheet("background-color: transparent; border-right: 1px solid #383838; border-bottom: 1px solid #383838;")
                if not is_fixed:
                    cell.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
                cl = QVBoxLayout(cell)
                cl.setContentsMargins(0,0,0,0)
                cl.setSpacing(0)
                cl.setAlignment(Qt.AlignCenter)
                cl.addWidget(widget)
                return cell

            # Left Header
            l_head = QLabel(title)
            l_head.setAlignment(Qt.AlignCenter)
            l_head.setStyleSheet("color: #999; font-weight: bold; background-color: transparent; border: none;") 
            
            head_cell = make_cell(l_head, is_header=True)
            head_cell.setFixedWidth(60) 
            rl.addWidget(head_cell)
            
            # Data Cols
            for w in cell_widgets:
                w.setStyleSheet(w.styleSheet() + "border: none;") 
                cell = make_cell(w)
                rl.addWidget(cell, 1)
            
            chart_v.addWidget(row_frame)

        # 1. Headers
        ws = []
        for h in col_headers:
            l = QLabel(h)
            l.setAlignment(Qt.AlignCenter)
            l.setStyleSheet("color: #aaa; font-size: 14px; background-color: transparent;")
            ws.append(l)
        add_stripe("", ws, bg_color="#252525", height=45)
        
        # 2. Ten Gods (Top)
        ws = []
        for i, c in enumerate(cols_data):
            tg = c.get('tenGod', '')
            l = QLabel(tg)
            l.setAlignment(Qt.AlignCenter)
            l.setStyleSheet("color: #aaa; font-size: 11px; background-color: transparent;")
            ws.append(l)
        add_stripe("十神", ws, height=35)
        
        # 3. Gan (Heavenly Stem)
        ws = []
        for c in cols_data:
            l = QLabel(c['gan'])
            l.setAlignment(Qt.AlignCenter)
            l.setStyleSheet(f"color: {c['ganColor']}; font-size: 26px; font-weight: bold; font-family: KaiTi; background-color: transparent;")
            ws.append(l)
        add_stripe("天干", ws, height=50)
        
        # 4. Zhi (Earthly Branch)
        ws = []
        for c in cols_data:
            l = QLabel(c['zhi'])
            l.setAlignment(Qt.AlignCenter)
            l.setStyleSheet(f"color: {c['zhiColor']}; font-size: 26px; font-weight: bold; font-family: KaiTi; background-color: transparent;")
            ws.append(l)
        add_stripe("地支", ws, height=50)
        
        # 5. Hidden Stems
        ws = []
        for c in cols_data:
            hidden = c.get('hidden', [])
            # Simplified vertical stack
            container = QWidget()
            vl = QVBoxLayout(container)
            vl.setContentsMargins(0,0,0,0)
            vl.setSpacing(2)
            vl.setAlignment(Qt.AlignCenter)
            
            for h in hidden:
                t = f"{h['stem']}{h['god']}"
                lbl = QLabel(t)
                lbl.setStyleSheet(f"color: #888; font-size: 11px;")
                lbl.setAlignment(Qt.AlignCenter)
                vl.addWidget(lbl)
            ws.append(container)
        add_stripe("藏干", ws, height=70) # Taller for hidden
        
        # 6. Na Yin
        ws = []
        for c in cols_data:
            l = QLabel(c.get('naYin', ''))
            l.setAlignment(Qt.AlignCenter)
            l.setStyleSheet("color: #aaa; font-size: 12px; background-color: transparent;")
            ws.append(l)
        add_stripe("纳音", ws, height=35)

        # 6.5 Kong Wang
        ws = []
        for c in cols_data:
            kw = c.get('kongWang', '')
            l = QLabel(kw)
            l.setAlignment(Qt.AlignCenter)
            l.setStyleSheet("color: #bbb; font-size: 13px; background-color: transparent;")
            ws.append(l)
        add_stripe("空亡", ws, height=35)
        
        # 7. Shen Sha (Calculate max height to fit all columns)
        max_ss_count = 0
        for c in cols_data:
            max_ss_count = max(max_ss_count, len(c.get('shenSha', [])))
        
        # Baseline 100px, or 22px per star + 20px padding
        row_height = max(100, (max_ss_count * 22) + 20)
        
        ws = []
        for c in cols_data:
            ss = c.get('shenSha', [])
            container = QWidget()
            container.setStyleSheet("background-color: transparent; border: none;")
            vl = QVBoxLayout(container)
            vl.setContentsMargins(0, 10, 0, 10)
            vl.setSpacing(4)
            vl.setAlignment(Qt.AlignCenter)
            
            for s in ss:
                lbl = QLabel(s)
                lbl.setStyleSheet("color: #ccc; font-size: 11px; border: none; background: transparent;")
                lbl.setAlignment(Qt.AlignCenter)
                vl.addWidget(lbl)
            ws.append(container)
            
        add_stripe("神煞", ws, bg_color="#2e2e2e", height=row_height)
        
        self.top_layout.addWidget(chart_container)


        
    def render_dayun_section(self, da_yun_list):
        self.clear_layout(self.bot_layout)
        
        line_color = "#383838"
        
        # 1. FIXED HEADER (Da Yun Row)
        header_container = QWidget()
        header_container.setStyleSheet(f"#HeaderGrid {{ border-top: 1px solid {line_color}; border-left: 1px solid {line_color}; }}")
        header_container.setObjectName("HeaderGrid")
        
        h_layout = QHBoxLayout(header_container)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(0)
        
        # Title Cell
        title_cell = QFrame()
        title_cell.setFixedSize(80, 100)
        title_cell.setStyleSheet(f"border-right: 1px solid {line_color}; border-bottom: 1px solid {line_color}; background: #1a1a1a;")
        tl = QVBoxLayout(title_cell)
        tl.setAlignment(Qt.AlignCenter)
        lbl_dy_title = QLabel("大运")
        lbl_dy_title.setStyleSheet("color: #e74c3c; font-size: 24px; font-weight: bold; border: none;") 
        tl.addWidget(lbl_dy_title)
        h_layout.addWidget(title_cell)
        
        for col, dy in enumerate(da_yun_list):
            if col >= 8: break
            
            dy_card = QFrame()
            dy_card.setFrameShape(QFrame.NoFrame)
            dy_card.setFixedSize(120, 100)
            
            is_active = False
            current_age = self.calculate_age(self.current_data['solarDate'])
            try:
                if int(dy['startAge']) <= current_age < int(dy['endAge']):
                    is_active = True
            except:
                pass
            
            bg = "#3e2723" if is_active else "#252525"
            style_base = f"background-color: {bg}; border-right: 1px solid {line_color}; border-bottom: 1px solid {line_color};"
            if is_active:
               style_base = f"background-color: {bg}; border: 2px solid #d35400;" 

            dy_card.setStyleSheet(style_base)
            
            l = QVBoxLayout(dy_card)
            l.setContentsMargins(0,10,0,10)
            l.setSpacing(5)
            l.setAlignment(Qt.AlignCenter)
            
            text_gz = dy['ganZhi']
            t1, t2 = (text_gz[0], text_gz[1]) if len(text_gz) >= 2 else ("", "")
            c1, c2 = self.get_element_color(t1), self.get_element_color(t2)
            
            gz = QLabel(f"<span style='color:{c1}'>{t1}</span><span style='color:{c2}'>{t2}</span>")
            gz.setStyleSheet("font-size: 24px; font-weight: bold; font-family: KaiTi; background: transparent; border: none;")
            gz.setAlignment(Qt.AlignCenter)
            
            info = QLabel(f"{dy['startAge']}岁\n{dy['startYear']}")
            info.setStyleSheet("color: #d35400; font-size: 14px; font-weight: bold; background: transparent; border: none;")
            info.setAlignment(Qt.AlignCenter)
            
            l.addWidget(gz)
            l.addWidget(info)
            h_layout.addWidget(dy_card)
        
        h_layout.addStretch()
        self.bot_layout.addWidget(header_container)
        
        # 2. TABLE VIEW BODY (High Performance)
        self.ln_table = QTableView()
        self.ln_model = LiuNianModel(da_yun_list)
        self.ln_table.setModel(self.ln_model)
        
        delegate = LiuNianDelegate(self.ln_table, self.get_element_color)
        self.ln_table.setItemDelegate(delegate)
        
        self.ln_table.verticalHeader().hide()
        self.ln_table.horizontalHeader().hide()
        self.ln_table.setShowGrid(False)
        self.ln_table.setFocusPolicy(Qt.NoFocus)
        self.ln_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.ln_table.setStyleSheet(f"QTableView {{ border: none; background: transparent; border-left: 1px solid {line_color}; border-top: 1px solid {line_color}; }}")
        
        self.ln_table.setMinimumHeight(600)
        
        body_container = QWidget()
        body_layout = QHBoxLayout(body_container)
        body_layout.setContentsMargins(0,0,0,0)
        body_layout.setSpacing(0)
        
        lbl_ln_title = QLabel("流年")
        lbl_ln_title.setStyleSheet(f"color: #e74c3c; font-size: 24px; font-weight: bold; border-left: 1px solid {line_color}; border-bottom: 1px solid {line_color}; border-right: 1px solid {line_color}; background-color: transparent;")
        lbl_ln_title.setAlignment(Qt.AlignCenter)
        lbl_ln_title.setFixedWidth(80) 
        lbl_ln_title.setFixedHeight(700) 
        
        body_layout.addWidget(lbl_ln_title)
        body_layout.addWidget(self.ln_table)
        body_layout.addStretch()
        
        self.bot_layout.addWidget(body_container)
        
        for c in range(8):
            self.ln_table.setColumnWidth(c, 120)
        
        for r in range(10):
            self.ln_table.setRowHeight(r, 70)
            
        self.ln_table.resizeColumnsToContents() 
        for c in range(8): self.ln_table.setColumnWidth(c, 120)

        # Fix Table Size to avoid internal scrollbars causing misalignment
        total_w = self.ln_model.columnCount() * 120
        total_h = self.ln_model.rowCount() * 70
        self.ln_table.setFixedSize(total_w, total_h)
        self.ln_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ln_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        now_year = self.get_current_bazi_year()
        found_idx = None
        for c in range(self.ln_model.columnCount()):
            for r in range(self.ln_model.rowCount()):
                data = self.ln_model.data(self.ln_model.index(r, c), Qt.UserRole)
                if data and data['year'] == now_year:
                    found_idx = self.ln_model.index(r, c)
                    break
            if found_idx: break
        
        if found_idx:
            QTimer.singleShot(100, lambda: self.ln_table.scrollTo(found_idx, QAbstractItemView.PositionAtCenter))
            
        self.ln_table.clicked.connect(self.on_table_clicked)

    def on_table_clicked(self, index):
        data = index.data(Qt.UserRole)
        if data:
            dy = self.ln_model.dayun_list[index.column()]
            self.show_year_detail(data, dy)

    def show_year_detail(self, liu_nian_data, da_yun_data):
        print(f"Clicked Year: {liu_nian_data['year']} {liu_nian_data['ganZhi']}")
        # Refresh the main chart pillars with the selected Luck context
        self.render_main_pillars(da_yun_data, liu_nian_data)
        
        # Notify other pages (e.g., Detailed Analysis)
        self.activePillarsChanged.emit(da_yun_data, liu_nian_data)
        
        # Update Interactions
        norm_dy = self.normalize_luck(da_yun_data)
        norm_ln = self.normalize_luck(liu_nian_data)
        dynamic_cols = [norm_dy, norm_ln]
        
        if self.current_data and 'interactions' in self.current_data:
             self.render_interactions(self.current_data['interactions'], dynamic_cols)
        
        # Scroll to Top
        self.scroll.verticalScrollBar().setValue(0)

    def clear_layout(self, layout):
        if not layout: return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def find_active_dayun(self, da_yun_list, current_age):
        for i, dy in enumerate(da_yun_list):
            try:
                start = int(dy['startAge'])
                end = int(dy['endAge'])
                if start <= current_age < end:
                    return i
            except ValueError:
                continue
        return -1

    def calculate_age(self, solar_date_str):
        import re
        match = re.search(r'\d{4}', solar_date_str)
        birth_year = int(match.group(0)) if match else 2000
        now_year = self.get_current_bazi_year()
        return now_year - birth_year + 1

    def get_fallback_liunian(self, current_year):
        base_year = 1984
        gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        diff = current_year - base_year
        while diff < 0: diff += 60
        offset = diff % 60
        g = gan[offset % 10]
        z = zhi[offset % 12]
        return {'ganZhi': g+z, 'ganColor': '#ccc', 'zhiColor': '#ccc'}

    def get_element_color(self, text):
        if text in "甲乙寅卯": return "#2ecc71"
        if text in "丙丁巳午": return "#e74c3c"
        if text in "戊己辰戌丑未": return "#a1887f"
        if text in "庚辛申酉": return "#f39c12"
        if text in "壬癸亥子": return "#3498db"
        return "#ccc"
