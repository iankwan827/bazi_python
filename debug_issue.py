from bazi_logic import calculate_bazi
import datetime

dt = datetime.datetime(1987, 9, 9, 1, 0)
gender = 'M'

print(f"Calculating for {dt} Gender: {gender}")
from lunar_python import Solar
solar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
lunar = solar.getLunar()
bazi = lunar.getEightChar()
yun = bazi.getYun(1 if gender == 'M' else 0)
da_yun_arr = yun.getDaYun()
print(f"Yun Object: {yun}")
print(f"Da Yun Arr (Length {len(da_yun_arr)}): {da_yun_arr}")
for dy in da_yun_arr:
    print(f"  DY: {dy.getGanZhi()} Age: {dy.getStartAge()}")

res = calculate_bazi(dt, gender)

print("--- Pillars ---")
for p in res['pillars']:
    print(f"{p['gan']}{p['zhi']}")

print("\n--- Da Yun List ---")
dyl = res['daYunList']
if not dyl:
    print("EMPTY LIST")
else:
    for dy in dyl:
        print(f"Age: {dy['startAge']} - {dy['ganZhi']}")

print("\n--- Da Yun Ranges (Now: 2026) ---")
dyl = res['daYunList']
import datetime
now_year = datetime.datetime.now().year
print(f"Current Year: {now_year}")

for i, dy in enumerate(dyl):
    s = dy['startYear']
    e = s + 10
    match = (s <= now_year < e)
    print(f"DY[{i}]: {dy['ganZhi']} ({s} - {e}) Match? {match}")

print("\n--- Result Current Da Yun ---")
print(res.get('currentDaYun'))
