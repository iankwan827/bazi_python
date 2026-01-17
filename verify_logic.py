from bazi_logic import calculate_bazi
from datetime import datetime
import traceback

try:
    # Test 1987-09-12 06:00
    dt = datetime(1987, 9, 12, 6, 0)
    data = calculate_bazi(dt, 'M')

    print(f"Solar: {data['solarDate']}")
    print(f"Pillars: {[p['gan']+p['zhi'] for p in data['pillars']]}")
    print(f"Day Master: {data['pillars'][2]['gan']}")
    print(f"Da Yun Count: {len(data['daYunList'])}")
    if len(data['daYunList']) > 0:
        print(f"First Dy: {data['daYunList'][0]['ganZhi']} Start: {data['daYunList'][0]['startAge']}")
        # print(f"Liu Nian for First Dy: {[ln['year'] for ln in data['daYunList'][0]['liuNian']]}")

    print("Interactions:", data['interactions'])

except Exception:
    traceback.print_exc()
