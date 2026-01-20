from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea, QHBoxLayout)
from PySide6.QtCore import Qt
import life_death_analysis
from lunar_python import Solar

class DetailedAnalysisPage(QWidget):
    """
    Active luck injection support.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.init_ui()
        self.current_data = None
        self.active_dy = None
        self.active_ln = None

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(20)
        self.content_layout.setAlignment(Qt.AlignTop)
        
        self.scroll.setWidget(self.content_widget)
        layout.addWidget(self.scroll)
        
        # Default Message
        self.lbl_placeholder = QLabel("请先进行排盘")
        self.lbl_placeholder.setAlignment(Qt.AlignCenter)
        self.lbl_placeholder.setStyleSheet("color: #666; font-size: 18px;")
        self.content_layout.addWidget(self.lbl_placeholder)

    def set_active_luck(self, dy, ln):
        """Called when user selects a year in Chart Page."""
        print(f"DetailedView: Active Luck Updated -> DY:{dy.get('ganZhi')} LN:{ln.get('ganZhi')}")
        self.active_dy = dy
        self.active_ln = ln
        if self.current_data:
            self.render_data(self.current_data, use_cached_luck=True)

    def render_data(self, data, use_cached_luck=False):
        self.current_data = data
        if not use_cached_luck:
             # Reset active luck to default (Current Time) if new chart loaded
             # But how to distinguish "New Chart" vs "Same Chart different tab"?
             # Assume if render_data is called from outside, it's a refresh.
             # Wait, usually render_data is called on "Pai Pan". 
             # So we should reset specific luck unless told otherwise.
             self.active_dy = None
             self.active_ln = None
        
        # Clear layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # 1. Prepare Pillars (Original + Current Luck)
        # We need to construct the full 6-pillar list that life_death_analysis expects.
        # Data structure from chart_view / bazi_logic:
        # data['pillars'] is list of 4 dicts.
        # We need to find current Da Yun and Liu Nian.
        # Since this page might be passive, we should ideally get the SAME context as the ChartPage.
        # For now, let's just use the current Da Yun / Liu Nian based on Date.
        # Or better, the chart_view should pass the 'active' pillars. 
        # But 'main_window' orchestrates. Let's use logic similar to chart_view.render_data default.
        
        pillars_4 = data['pillars']
        
        current_dy = self.active_dy
        current_ln = self.active_ln
        
        if not current_dy or not current_ln:
            # Default to Current Date Logic if no specific selection
            import datetime
            da_yun_list = data['daYunList']
            current_date_str = data['solarDate'] # "YYYY-MM-DD ..."
            
            # Li Chun Logic Function
            def get_bazi_year(dt_now):
                """
                Determine Bazi Year. If before Li Chun of current year, return year-1.
                Uses lunar_python for precise solar term calculation.
                """
                gregorian_year = dt_now.year
                try:
                    # Get Li Chun for current Gregorian year
                    # Logic: Li Chun is usually Feb 3-5.
                    # Create Solar date for approx Li Chun to find accurate term time
                    s = Solar.fromYmd(gregorian_year, 2, 4)
                    l = s.getLunar()
                    jq_table = l.getJieQiTable()
                    
                    if '立春' in jq_table:
                        lc_solar = jq_table['立春']
                        # Convert to datetime for comparison
                        lc_dt = datetime.datetime(lc_solar.getYear(), lc_solar.getMonth(), lc_solar.getDay(), 
                                                  lc_solar.getHour(), lc_solar.getMinute(), lc_solar.getSecond())
                        
                        if dt_now < lc_dt:
                            return gregorian_year - 1
                        else:
                            return gregorian_year
                    else:
                        # Fallback (should not happen for Feb 4)
                        # If simple check
                        if dt_now.month < 2 or (dt_now.month == 2 and dt_now.day < 4):
                            return gregorian_year - 1
                        return gregorian_year
                except Exception as e:
                    print(f"Li Chun Calc Error: {e}")
                    # Fallback to simple logic
                    if dt_now.month < 2 or (dt_now.month == 2 and dt_now.day < 4):
                        return gregorian_year - 1
                    return gregorian_year

            # Calculate Age
            import re
            match = re.search(r'\d{4}', current_date_str)
            birth_year = int(match.group(0)) if match else 2000
            
            now_dt = datetime.datetime.now()
            bazi_year = get_bazi_year(now_dt)
            current_year_real = now_dt.year # For age calc, usually nominal age uses straight year diff
            # Bazi Age (Nominal) = Current Bazi Year - Birth Year + 1 
            # Or just use simple year? Usually Nominal Age aligns with Ganzhi year.
            current_age = bazi_year - birth_year + 1
            
            for dy in da_yun_list:
                try:
                    if int(dy['startAge']) <= current_age < int(dy['endAge']):
                        current_dy = dy
                        break
                except: pass
            
            if current_dy:
                for ln in current_dy['liuNian']:
                    if ln['year'] == bazi_year:
                        current_ln = ln
                        break
        
        # Construct 6 pillars
        # Normalize to match expected format (gan, zhi, tenGod, hidden)
        # existing pillars have these.
        # dy/ln from daYunList have 'ganZhi', 'tenGod', 'hidden' ...
        
        full_pillars = [p for p in pillars_4]
        
        if current_dy:
            full_pillars.append(self.format_luck_pillar(current_dy))
        if current_ln:
            full_pillars.append(self.format_luck_pillar(current_ln))
            
        # DEBUG: Print pillars passed to analysis
        for idx, p in enumerate(full_pillars):
            print(f"DEBUG Analysis Pillar {idx}: Gan={p.get('gan')} Zhi={p.get('zhi')} TenGod={p.get('tenGod')}")
            
        # 2. Run Analysis (Current Time Slice)
        results = life_death_analysis.analyze_risks(full_pillars, data.get('info'))
        
        # 3. Get / Process Forecast (Future Years)
        if not use_cached_luck or not hasattr(self, 'cached_forecast'):
             self.cached_forecast = life_death_analysis.get_future_risk_years(data)
             
        # Group Forecast by Risk Title
        grouped_forecast = {}
        if self.cached_forecast:
            for item in self.cached_forecast:
                k = item['risk'] # Full title
                if k not in grouped_forecast: grouped_forecast[k] = []
                grouped_forecast[k].append(item)
            
        # 4. Check if we have anything to show
        if not results and not grouped_forecast:
             self.content_layout.addStretch()
             return

        # Common Warning Header
        warning_lbl = QLabel("⚠️ 检测到以下高危风险 (含未来年份预测)，可能会有生命危险：")
        warning_lbl.setStyleSheet("color: #c0392b; font-size: 16px; font-weight: bold; margin-bottom: 5px;")
        self.content_layout.addWidget(warning_lbl)
        
        display_idx = 1
        
        # Display Forecast Results (consolidated) FIRST (as requested for "prompting years")
        import datetime
        now = datetime.datetime.now()
        
        # Robust Li Chun Logic for Forecast Timeline - REMOVED to align with Web Logic
        # Web uses Gregorian Year (new Date().getFullYear())
        current_year = now.year
        
        def get_formatted_years(items_to_format):
            if not items_to_format: return ""
            # Treat 'BOTH' as 'DY' for grouping purposes to avoid splitting ranges
            dy_risks = [x for x in items_to_format if x.get('trigger_type') in ('DY', 'BOTH')]
            # 'LN' only risks remain separate
            other_risks = [x for x in items_to_format if x.get('trigger_type') == 'LN']
            
            segments = []
            from collections import defaultdict
            grouped_by_dy = defaultdict(list)
            for x in dy_risks:
                grouped_by_dy[x.get('dy_name', '未知运')].append(x)
            for dy_name, yrs in grouped_by_dy.items():
                yrs.sort(key=lambda x: x['year'])
                if not yrs: continue
                
                # Check for continuity or just show range
                start = yrs[0]['year']
                end = yrs[-1]['year']
                
                # If we have a significant chunk (e.g. >5 years), treat as Da Yun Block
                if len(yrs) >= 5:
                    segments.append(f"<b>{dy_name}大运({start}-{end})</b>")
                else:
                    y_str = "、".join([str(y['year']) for y in yrs])
                    segments.append(f"<b>{dy_name}运内({y_str})</b>")
                    
            for x in other_risks:
                segments.append(f"{x['year']}({x['ganZhi']})")
            return "，".join(segments)

        
        # Display Current Slice Results (Eating God, etc. - STATIC RISKS) - FIRST (Moved UP)
        # Identify static risks from initial analysis
        static_risks = [r for r in results if r.get('trigger_type') == 'ORIGINAL']
        
        # Sort Static Risks by Category Priority (RISK > GOOD > INFO)
        # Assuming category field exists (default RISK)
        cat_order = {'RISK': 1, 'GOOD': 2, 'INFO': 3}
        static_risks.sort(key=lambda x: cat_order.get(x.get('category', 'RISK'), 99))

        for res in static_risks:
            self.add_alert_card(res, display_idx)
            display_idx += 1
            
        for title, items in grouped_forecast.items():
            items.sort(key=lambda x: x['year'])
            past_items = [x for x in items if x['year'] < current_year]
            current_items = [x for x in items if x['year'] == current_year]
            future_items = [x for x in items if x['year'] > current_year]
            
            desc_parts = []
            if past_items:
                p_str = get_formatted_years(past_items)
                desc_parts.append(f"<span style='color: #7f8c8d;'>已过年份：{p_str}</span>")
            
            if current_items:
                c_str = get_formatted_years(current_items)
                desc_parts.append(f"<span style='color: #c0392b; font-weight: bold;'>当前年份：{c_str}</span>")

            if future_items:
                f_str = get_formatted_years(future_items)
                desc_parts.append(f"<span style='color: #e67e22;'>未来年份：{f_str}</span>")
            
            years_html = "；".join(desc_parts)
            base_desc = items[0]['desc']
            
            res = {
                'title': title, 
                'description': f"{years_html}。断语：{base_desc}",
                # Modify description formatting in add_alert_card to handle HTML if needed
                # add_alert_card expects plain text mostly but I inject HTML usually? 
                # Let's check add_alert_card. It constructs HTML string.
                # If I put HTML in description, it might break if it expects plain text?
                # add_alert_card: f" : {res['description']} "
                # So it just appends. HTML should be fine.
                'probability': '极高'
            }
            self.add_alert_card(res, display_idx)
            display_idx += 1
            
        # Display Current Slice Results (Eating God, etc. - STATIC RISKS) logic moved UP
        
        # If 'results' contains everything (it does for analyze_risks), we just show them.
        # But wait, analyze_risks() triggers check_eating_god_meets_owl_logic() based on 4 pillars.
        # So it effectively returns 'Static' risks only (as len < 6 usually, or if passed 6, indices 4/5 are empty/mock?)
        # Actually analyze_risks passes 'pillars'. 
        # If the user is just viewing the chart, 'pillars' usually has 4 items (Year, Month, Day, Hour).
        # So len < 6.
        # check_eating_god_meets_owl_logic returns [] if len < 6?
        # NO. It was returning for < 4. I changed it to return [] if len < 4.
        # So for 4 pillars, it returns Static results (indices 0-3).
        # So 'results' will contain Static risks.
        
          
        
        self.content_layout.addStretch()

    def format_luck_pillar(self, luck_obj):
        gz = luck_obj.get('ganZhi', '')
        g = gz[0] if len(gz)>0 else ''
        z = gz[1] if len(gz)>1 else ''
        return {
            'gan': g,
            'zhi': z,
            'tenGod': luck_obj.get('tenGod', ''),
            'hidden': luck_obj.get('hidden', []),
            'ganZhi': gz,
            'naYin': luck_obj.get('naYin', '')
        }

    def add_alert_card(self, res, idx):
        # Refined Style: No Background Box, but Color-Coded Titles + Better Alignment
        # category: RISK (Red), GOOD (Green), INFO (Blue)
        category = res.get('category', 'RISK')
        
        color_map = {
            'RISK': '#e74c3c', # Red
            'GOOD': '#2ecc71', # Green
            'INFO': '#3498db'  # Blue
        }
        title_color = color_map.get(category, '#e74c3c')
        
        # Using div/p for layout. 
        # Title on one line.
        # Description on next line with indentation.
        
        text = (f"<div style='margin-bottom: 8px;'>"
                f"  <div style='color: {title_color}; font-weight: bold; font-size: 16px; margin-bottom: 2px;'>"
                f"    {idx}. {res['title']}"
                f"  </div>"
                f"  <div style='color: #bdc3c7; font-size: 14px; margin-left: 22px; line-height: 1.4;'>"
                f"    {res['description']} "
                f"    <span style='color: #f39c12; font-size: 12px;'>(应验率: {res['probability']})</span>"
                f"  </div>"
                f"</div>")
                
        lbl = QLabel(text)
        lbl.setWordWrap(True) 
        lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        # Margin already handled by div, but adding container margin to be safe
        lbl.setStyleSheet("margin-bottom: 5px;") 
        self.content_layout.addWidget(lbl)
