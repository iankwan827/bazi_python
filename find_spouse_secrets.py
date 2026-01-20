
import sys
import os
from datetime import datetime, timedelta
from bazi_logic import get_bazi_chart
from life_death_analysis import analyze_risks, get_future_risk_years

# Mock processed pillars structure for analysis
def mock_analyze(chart):
    pillars = []
    for p in chart['pillars']:
         # Simplified mock, assuming basic keys
         pillars.append({
             'gan': p['gan'],
             'zhi': p['zhi'],
             'tenGod': p.get('tenGod', ''), # Assuming bazi_logic populates this or we mock it
             'hidden': p.get('hidden', []),
             'shenSha': p.get('shenSha', [])
         })
    return analyze_risks(pillars)

def run_search():
    start_date = datetime(1980, 1, 1)
    end_date = datetime(2030, 12, 31)
    curr = start_date

    found_s8 = False
    found_s9 = False

    print("Searching for Secret 8 (Double Yang Ren)...")
    
    # We need a Day Master Yang Ren map locally to speed up pre-check if possible, 
    # but `get_bazi_chart` does heavy lifting. 
    # Let's iterate days.
    
    while curr < end_date:
        # Optimization: Only check every 10 days? No, Day Branch changes daily.
        # Check every day for a year, if not found then jump?
        # Let's just run for a few years.
        
        try:
            chart = get_bazi_chart(curr.year, curr.month, curr.day, 12) # Noon
            risks = mock_analyze(chart)
            
            # Check for Secret 8
            for r in risks:
                if "秘诀：日支羊刃他处见" in r['title'] and not found_s8:
                    print(f"\n[FOUND Secret 8] Date: {curr.strftime('%Y-%m-%d %H:%M')}")
                    print(f"Chart: {chart['pillars'][0]['ganZhi']} {chart['pillars'][1]['ganZhi']} {chart['pillars'][2]['ganZhi']} {chart['pillars'][3]['ganZhi']}")
                    print(f"Risk: {r['title']} - {r['description']}")
                    found_s8 = True
            
            # Check for Secret 9 (Dynamic)
            # This requires running `get_future_risk_years` which is heavy.
            # Pre-condition: Day Branch MUST be Yang Ren.
            # Let's check logic: analyze_risks doesn't check dynamic, but we can check if Day is Yang Ren manually first.
            
            if not found_s9:
                # Manual Check Day Yang Ren
                dm = chart['pillars'][2]['gan']
                dz = chart['pillars'][2]['zhi']
                YANG_REN = {'甲': '卯', '乙': '寅', '丙': '午', '丁': '巳', '戊': '午', '己': '巳', '庚': '酉', '辛': '申', '壬': '子', '癸': '亥'}
                if YANG_REN.get(dm) == dz:
                    # Potential candidate. Check future risks.
                    # We need Da Yun. `get_bazi_chart` returns full object with daYunList?
                    # Yes, usually.
                    
                    forecast = get_future_risk_years(chart)
                    for f in forecast:
                        if "秘诀：配偶血光" in f['risk']:
                            print(f"\n[FOUND Secret 9] Date: {curr.strftime('%Y-%m-%d %H:%M')}")
                            print(f"Chart: {chart['pillars'][0]['ganZhi']} {chart['pillars'][1]['ganZhi']} {chart['pillars'][2]['ganZhi']} {chart['pillars'][3]['ganZhi']}")
                            print(f"Trigger Year: {f['year']} ({f['ganZhi']})")
                            print(f"Risk: {f['risk']} - {f['desc']}")
                            found_s9 = True
                            break
                            
            if found_s8 and found_s9:
                break
                
        except Exception as e:
            # print(e)
            pass
            
        curr += timedelta(days=1)
        
    print("\nSearch complete.")

if __name__ == "__main__":
    run_search()
