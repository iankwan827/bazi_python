import sys
import os
print("CWD:", os.getcwd())
print("Sys Path:", sys.path)

try:
    import chart_page
    print("ChartPage File:", chart_page.__file__)
    
    # Read the file to see if it has the new header
    with open(chart_page.__file__, 'r', encoding='utf-8') as f:
        content = f.read()
        if "大运流年总表 (80年运程) [已更新]" in content:
            print("STATUS: File HAS the new update string.")
        elif "大运排盘" in content:
            print("STATUS: File has OLD 'Da Yun Pai Pan' string.")
        else:
            print("STATUS: Header not found (weird).")
            
except ImportError as e:
    print("Import Error:", e)
