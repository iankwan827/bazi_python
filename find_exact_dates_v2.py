
from datetime import datetime, timedelta
from lunar_python import Solar, Lunar

def find_dates():
    # Case 1: Secret 8 - Double Yang Ren
    # Year: Wu Wu (1978). Day: Bing Wu.
    # 1978 starts Feb 7 (Lunar).
    start = datetime(1978, 2, 7)
    end = datetime(1979, 1, 27)
    curr = start
    found_1 = False
    
    while curr < end:
        solar = Solar.fromYmd(curr.year, curr.month, curr.day)
        lunar = solar.getLunar()
        if lunar.getYearInGanZhi() == '戊午' and lunar.getDayInGanZhi() == '丙午':
            print(f"Case 1 (Secret 8 - Day Bing Wu, Year Wu Wu): {curr.strftime('%Y-%m-%d 12:00')}")
            found_1 = True
            break
        curr += timedelta(days=1)
        
    # Case 2: Secret 9 - Day Sitting Yang Ren (Ren Zi) + Clash (Wu)
    # Let's find a Ren Zi day.
    # To demonstrate dynamic clash, we can pick a recent date.
    # 1990?
    start = datetime(1990, 1, 1)
    end = datetime(1990, 12, 31)
    curr = start
    while curr < end:
        solar = Solar.fromYmd(curr.year, curr.month, curr.day)
        lunar = solar.getLunar()
        if lunar.getDayInGanZhi() == '壬子':
            print(f"Case 2 (Secret 9 - Day Ren Zi, Check for Wu Clash): {curr.strftime('%Y-%m-%d 12:00')}")
            break
        curr += timedelta(days=1)

if __name__ == "__main__":
    find_dates()
