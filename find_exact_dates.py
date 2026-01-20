
from datetime import datetime, timedelta
from lunar_python import Solar, Lunar

def find_dates():
    # Case 1: Year Bing Yin (1986), Month Ding Mao, Day Jia Mao
    # 1986 is Bing Yin.
    start = datetime(1986, 3, 1)
    end = datetime(1986, 4, 15)
    curr = start
    while curr < end:
        solar = Solar.fromYmd(curr.year, curr.month, curr.day)
        lunar = solar.getLunar()
        if lunar.getYearInGanZhi() == '丙寅' and lunar.getMonthInGanZhi() == '丁卯' and lunar.getDayInGanZhi() == '甲卯':
            print(f"Case 1 (Secret 8): {curr.strftime('%Y-%m-%d 12:00')}")
            break
        curr += timedelta(days=1)
        
    # Case 2: secret 9
    # Year/Month don't matter much to trigger day clash, just need Geng You Day.
    # But let's use the one from test: Ren Zi Year, Gui Chou Month -> 1972?
    # 1972 is Ren Zi.
    # Gui Chou month is Jan 1973 (Lunar 12th month of 1972) or similar.
    # Let's search 1972/1973.
    start = datetime(1972, 11, 1)
    end = datetime(1973, 2, 28)
    curr = start
    while curr < end:
        solar = Solar.fromYmd(curr.year, curr.month, curr.day)
        lunar = solar.getLunar()
        # verify month/year rough match
        # Just find Geng You day.
        if lunar.getDayInGanZhi() == '庚酉':
            print(f"Case 2 (Secret 9): {curr.strftime('%Y-%m-%d 12:00')}")
            break
        curr += timedelta(days=1)

if __name__ == "__main__":
    find_dates()
