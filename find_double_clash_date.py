
from datetime import datetime, timedelta
from lunar_python import Solar, Lunar

def find_dates():
    # Target: Month Wu (Horse), Day Zi (Rat). Hour Wu (fixed at 12:00).
    # Month Wu is roughly June (Lunar 5th month).
    start = datetime(1990, 5, 1)
    end = datetime(1990, 8, 1)
    
    print("Searching for Month Wu + Day Zi in 1990...")
    curr = start
    while curr < end:
        solar = Solar.fromYmd(curr.year, curr.month, curr.day)
        lunar = solar.getLunar()
        m_zhi = lunar.getMonthInGanZhi()[1]
        d_zhi = lunar.getDayInGanZhi()[1]
        
        if m_zhi == '午' and d_zhi == '子':
            print(f"FOUND: {curr.strftime('%Y-%m-%d')} (Month {lunar.getMonthInGanZhi()}, Day {lunar.getDayInGanZhi()})")
            print(f"Set time to 12:00 (Wu Hour) for double clash.")
            break
        curr += timedelta(days=1)

if __name__ == "__main__":
    find_dates()
