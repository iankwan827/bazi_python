
from datetime import datetime, timedelta
from lunar_python import Solar

def debug_dates():
    # Check 1978-05-18
    d1 = datetime(1978, 5, 18)
    s1 = Solar.fromYmd(d1.year, d1.month, d1.day)
    l1 = s1.getLunar()
    print(f"1978-05-18: {l1.getYearInGanZhi()} {l1.getMonthInGanZhi()} {l1.getDayInGanZhi()}")
    
    # Check for Bing Wu (Year 1978)
    # Search whole year
    curr = datetime(1978, 1, 1)
    end = datetime(1978, 12, 31)
    
    print("\nSearching for Bing Wu days in 1978:")
    while curr < end:
        s = Solar.fromYmd(curr.year, curr.month, curr.day)
        l = s.getLunar()
        if l.getDayInGanZhi() == '丙午':
            print(f"FOUND Bing Wu: {curr.strftime('%Y-%m-%d')}")
        curr += timedelta(days=1)

    # Check for Ren Zi (Year 1990)
    print("\nSearching for Ren Zi days in 1990:")
    curr = datetime(1990, 1, 1)
    end = datetime(1990, 12, 31)
    while curr < end:
        s = Solar.fromYmd(curr.year, curr.month, curr.day)
        l = s.getLunar()
        if l.getDayInGanZhi() == '壬子':
             print(f"FOUND Ren Zi: {curr.strftime('%Y-%m-%d')}")
        curr += timedelta(days=1)

if __name__ == "__main__":
    debug_dates()
