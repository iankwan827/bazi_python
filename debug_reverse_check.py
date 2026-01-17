from lunar_python import Solar
import datetime

def check_2002():
    start = datetime.date(2002, 2, 1) # Ren Yin month starts around Feb 4
    end = datetime.date(2002, 3, 10)
    
    target_pillars = "壬午 壬寅 丁未 辛丑"
    print(f"Target: {target_pillars}")
    
    found = False
    curr = start
    while curr <= end:
        # Check standard time (e.g. 12:00)
        # Hour: Xin Chou -> 02:00
        solar = Solar.fromYmdHms(curr.year, curr.month, curr.day, 2, 0, 0)
        lunar = solar.getLunar()
        bazi = lunar.getEightChar()
        
        y = bazi.getYearGan() + bazi.getYearZhi()
        m = bazi.getMonthGan() + bazi.getMonthZhi()
        d = bazi.getDayGan() + bazi.getDayZhi()
        t = bazi.getTimeGan() + bazi.getTimeZhi()
        
        current_pillars = f"{y} {m} {d} {t}"
        
        if d == "丁未":
            print(f"[{curr}] {current_pillars}  <-- Found Ding Wei Day")
        
        if current_pillars == target_pillars:
            print(f"MATCH FOUND: {curr} 02:00")
            found = True
            
        curr += datetime.timedelta(days=1)

    if not found:
        print("No exact match found in Feb/Mar 2002.")

if __name__ == "__main__":
    check_2002()
