from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QHBoxLayout, QGridLayout)
from PySide6.QtCore import Qt
from bazi_logic import (get_gong_jia_relations, get_interactions, 
                        calculate_body_strength, calculate_yong_xi_ji, get_five_element_profile,
                        get_tomb_warehouse_status, calculate_global_scores)

class JudgmentFormulasPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(15)
        
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)
        
        # Styles
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.scroll_content.setStyleSheet("background: #1e1e1e;")

    def render_data(self, data):
        # Clear existing items
        self.clear_layout(self.scroll_layout)
        
        # Header
        header = QLabel("原局断事口诀")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #d35400; margin-bottom: 20px;")
        
        # We need a layout for the whole page. 
        # But wait, self.scroll_layout is a QVBoxLayout currently.
        # We should put header in it, then a QWidget containing a QGridLayout for the items.
        
        self.scroll_layout.addWidget(header)
        
        # 0. Preparation
        pillars = data.get('pillars', [])
        
        # 1. Original Chart Calculation
        bs = calculate_body_strength(pillars) # Just 4 pillars
        yxj = calculate_yong_xi_ji(pillars, bs)
        profile = get_five_element_profile(pillars)
        
        extra = ""
        if bs.get('isGuanYin'): extra = " <span style='font-size:13px; color:#aaa;'>(官印局)</span>"
            
        yxj_html = ""
        if yxj['yong']:
            mode_extras = ""
            if yxj.get('type_desc'):
                mode_extras = f"-{yxj['type_desc']}"
            
            yxj_html = f" <span style='font-size:14px; color:#aaa;'>[{yxj['mode']}{mode_extras}] " \
                       f"<span style='color:#27ae60;'>用:{yxj['yong']}</span> " \
                       f"<span style='color:#2980b9;'>喜:{yxj['xi']}</span> " \
                       f"<span style='color:#c0392b;'>忌:{yxj['ji']}</span></span>"
                       
        bs_html = f"<span style='color: #d35400; font-weight: bold;'>身强身旺：</span><span style='color: #e74c3c; font-weight: bold;'>{bs['level']}</span>{extra}{yxj_html}"
        

        p_html = ""
        for p in profile:
            c = '#d35400' if p['isStrong'] else '#7f8c8d'
            w = 'bold' if p['isStrong'] else 'normal'
            p_html += f"<span style='color:{c}; font-weight:{w}; margin-right:8px;'>{p['element']}({p['tenGod']}){'强' if p['isStrong'] else '弱'}</span>"
        
        

        # New: Tomb/Warehouse Status
        scores = calculate_global_scores(pillars)
        tomb_status = get_tomb_warehouse_status(pillars, scores)

        b_status_html = ""
        if tomb_status:
            b_status_html += "<div style='margin-top:6px; font-size:13px; color:#aaa;'>地支状态: "
            pillars_names = ["年", "月", "日", "时"]
            found_any = False
            
            # Label Mapping for Display
            # Chen -> Water, Xu -> Fire+Earth, Chou -> Metal, Wei -> Wood
            TYPE_LABELS = {
                '辰': '水',
                '戌': '火土',
                '丑': '金',
                '未': '木'
            }
            
            for idx, status in tomb_status.items():
                if idx < len(pillars_names):
                    p_name = pillars_names[idx]
                    zhi_char = pillars[idx]['zhi']
                    
                    element_label = TYPE_LABELS.get(zhi_char, '')
                    status_text = status['desc'] # '库' or '墓'
                    
                    # status['type'] is 'Warehouse' or 'Tomb'
                    # User wants: "辰水库", "戌火土墓"
                    # Format: zhi_char + element_label + status_text
                    
                    full_label = f"{zhi_char}{element_label}{status_text}"
                    
                    if status['type'] == 'Warehouse':
                        b_status_html += f"<span style='color:#27ae60; margin-right:5px;'>[{p_name}:{full_label}]</span>"
                        found_any = True
                    else:
                        b_status_html += f"<span style='color:#7f8c8d; margin-right:5px;'>[{p_name}:{full_label}]</span>"
                        found_any = True
            b_status_html += "</div>"
            if not found_any: b_status_html = ""

        orig_lbl = QLabel(f"<div>{bs_html}</div><div style='margin-top:5px; font-size:14px;'><span style='font-weight:bold; color:#ccc;'>五行走势: </span>{p_html}</div>{b_status_html}")
        orig_lbl.setTextFormat(Qt.RichText)
        orig_lbl.setWordWrap(True)
        orig_lbl.setStyleSheet("padding: 12px 10px; border-bottom: 1px solid #333; font-size: 15px;")
        self.scroll_layout.addWidget(orig_lbl)

        # 2. Dynamic 6 Pillars (If available)
        dy_pillar = data.get('dayun')
        ln_pillar = data.get('liunian')
        
        if not dy_pillar and data.get('currentDaYun'):
            dy_data = data['currentDaYun']
            dy_pillar = {'gan': dy_data['gan'], 'zhi': dy_data['zhi']}
            import datetime
            now_year = datetime.datetime.now().year
            ln_data = next((ln for ln in dy_data.get('liuNian', []) if ln['year'] == now_year), None)
            if ln_data: ln_pillar = {'gan': ln_data['gan'], 'zhi': ln_data['zhi']}

        if dy_pillar and ln_pillar:
             calc_pillars_6 = pillars[:]
             calc_pillars_6.append(dy_pillar)
             calc_pillars_6.append(ln_pillar)
             
             bs6 = calculate_body_strength(calc_pillars_6)
             yxj6 = calculate_yong_xi_ji(calc_pillars_6, bs6)
             profile6 = get_five_element_profile(calc_pillars_6)
             
             extra6 = ""
             if bs6.get('isGuanYin'): extra6 = " <span style='font-size:13px; color:#aaa;'>(官印局)</span>"
             
             yxj6_html = ""
             if yxj6['yong']:
                mode_extras6 = ""
                if yxj6.get('type_desc'):
                    mode_extras6 = f"-{yxj6['type_desc']}"
                yxj6_html = f" <span style='font-size:14px; color:#aaa;'>[{yxj6['mode']}{mode_extras6}] " \
                           f"<span style='color:#27ae60;'>用:{yxj6['yong']}</span> " \
                           f"<span style='color:#2980b9;'>喜:{yxj6['xi']}</span> " \
                           f"<span style='color:#c0392b;'>忌:{yxj6['ji']}</span></span>"

             bs6_html = f"<span style='color: #d35400; font-weight: bold;'>六柱强弱：</span><span style='color: #e74c3c; font-weight: bold;'>{bs6['level']}</span>{extra6}{yxj6_html}"
             p6_html = ""
             for p in profile6:
                c = '#d35400' if p['isStrong'] else '#7f8c8d'
                w = 'bold' if p['isStrong'] else 'normal'
                p6_html += f"<span style='color:{c}; font-weight:{w}; margin-right:8px;'>{p['element']}({p['tenGod']}){'强' if p['isStrong'] else '弱'}</span>"
             
             alert_html = ""
             if bs6.get('alerts'):
                 for a in bs6['alerts']:
                     alert_html += f"<div style='color:#ff4444; font-weight:bold; margin-top:4px;'>{a}</div>"

             dyn_lbl = QLabel(f"<div>{bs6_html}</div><div style='margin-top:5px; font-size:14px;'><span style='font-weight:bold; color:#ccc;'>五行走势: </span>{p6_html}</div>{alert_html}")
             dyn_lbl.setTextFormat(Qt.RichText)
             dyn_lbl.setWordWrap(True)
             dyn_lbl.setStyleSheet("padding: 12px 10px; border-bottom: 1px solid #333; font-size: 15px;")
             self.scroll_layout.addWidget(dyn_lbl)

        # 3. Gong Jia Section
        gj = get_gong_jia_relations(pillars)
        all_items = []
        def process_items(lst, is_sep):
            for item in lst:
                for rel in item['relations']:
                    if rel['type'] in ['拱', '夹', '倒夹']:
                        flat_item = item.copy()
                        flat_item['rel'] = rel
                        flat_item['is_sep'] = is_sep
                        all_items.append(flat_item)
        process_items(gj['adjacent'], False)
        process_items(gj['separated'], True)
        
        if all_items:
             html_parts = ["<span style='color: #d35400; font-weight: bold;'>拱夹：</span>"]
             for item in all_items:
                 c = self.get_color(item['rel']['char'])
                 part = f"<span style='color:#aaa'>{item['rel']['type']}</span><span style='color:{c}; font-weight:bold;'>{item['rel']['char']}</span><span style='color:#666; font-size:12px;'>({item['p1']}-{item['p2']}{'/隔' if item['is_sep'] else ''})</span>"
                 html_parts.append(part)
             full_html = "&nbsp;&nbsp;&nbsp;".join(html_parts)
             lbl = QLabel(full_html)
             lbl.setWordWrap(True)
             lbl.setTextFormat(Qt.RichText)
             lbl.setStyleSheet("padding: 12px 10px; border-bottom: 1px solid #333; font-size: 15px; background: transparent;")
             self.scroll_layout.addWidget(lbl)
             
        # 4. He Hua Judgments Section
        interactions = get_interactions(pillars)
        if interactions.get('judgments'):
            j_html = "<span style='color: #d35400; font-weight: bold;'>命局断语：</span><br>"
            for j in interactions['judgments']:
                j_html += f"<span style='color: #e74c3c; font-size: 14px;'>• {j}</span><br>"
            j_lbl = QLabel(j_html)
            j_lbl.setTextFormat(Qt.RichText)
            j_lbl.setWordWrap(True)
            j_lbl.setStyleSheet("padding: 12px 10px; border-bottom: 1px solid #333; font-size: 15px; background: transparent;")
            self.scroll_layout.addWidget(j_lbl)

        self.scroll_layout.addStretch()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def get_color(self, char):
        colors = {
            '寅': '#27ae60', '卯': '#27ae60',
            '巳': '#c0392b', '午': '#c0392b',
            '辰': '#a1887f', '戌': '#a1887f', '丑': '#a1887f', '未': '#a1887f',
            '申': '#b8860b', '酉': '#b8860b',
            '亥': '#2980b9', '子': '#2980b9'
        }
        return colors.get(char, '#ccc')
