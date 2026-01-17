from bazi_logic import calculate_bazi
from datetime import datetime
from chart_page import ChartPage
print("ChartPage imported")

date = datetime(1987, 7, 20, 9, 30) # Example date
data = calculate_bazi(date, 'M')

print("Da Yun List Length:", len(data['daYunList']))
for dy in data['daYunList']:
    print(f"Da Yun: {dy['ganZhi']} ({dy['startAge']}) - Liu Nian Count: {len(dy['liuNian'])}")
