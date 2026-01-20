import json
import os

json_path = r'e:\SD\bazi - 副本\bazi_python\year_map.json'
js_path = r'e:\SD\bazi - 副本\bazi_new_web\js\year_map.js'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

js_content = "export const YEAR_MAP = " + json.dumps(data, indent=4, ensure_ascii=False) + ";"

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Sync complete.")
