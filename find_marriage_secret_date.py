
from datetime import datetime, timedelta
from lunar_python import Solar, Lunar

def find_dates():
    # Case 1: Male (Jia DM) + 2+ Ji (Zheng Cai) Stems
    # Ji Year (e.g. 1979 Ji Wei, 1989 Ji Si, 1999 Ji Mao, 2009 Ji Chou, 2019 Ji Hai).
    # Month Ji? Or Hour Ji?
    # Target: Year Ji + Month Ji + Day Jia. (Two Ji combine Jia).
    # 1979 is Ji Wei.
    # Month Ji Si (May/June).
    # Day Jia?
    
    print("\nSearching for Male Case (Jia DM + 2 Ji Stems)...")
    start = datetime(1979, 1, 1)
    end = datetime(1979, 12, 31)
    curr = start
    found_1 = False
    
    while curr < end:
        solar = Solar.fromYmd(curr.year, curr.month, curr.day)
        lunar = solar.getLunar()
        y_gan = lunar.getYearInGanZhi()[0]
        m_gan = lunar.getMonthInGanZhi()[0]
        d_gan = lunar.getDayInGanZhi()[0]
        
        # We need Day Jia. And Year=Ji, Month=Ji? Or just Count(Ji) >= 2 in Y/M/H?
        # Year is Ji (1979). so count is at least 1.
        # If Month is Ji, then count=2.
        # If Month isn't Ji, Hour must be Ji (Jia Day's Hour??)
        # Wu Hu Dun: Jia Ji pairs.
        # Day Jia -> Hour start Jia Zi... Ji Si (09:00-11:00).
        # So ANY Jia Day in Ji Year has 2 Ji if born at Snake Hour (Ji Si).
        
        if d_gan == '甲' and y_gan == '己':
            print(f"FOUND Candidate: {curr.strftime('%Y-%m-%d')} (Jia Day in Ji Year)")
            print(f"Use Hour: 09:00-11:00 (Ji Si Hour) -> Total 2 Ji (Year+Hour).")
            found_1 = True
            break
        curr += timedelta(days=1)


    # Case 2: Female (Yi DM) + 2+ Geng (Zheng Guan) Stems
    # Year Geng (1980 Geng Shen, 1990 Geng Wu, 2000 Geng Chen).
    # 1990 is Geng Wu.
    # Day Yi.
    # Hour Geng? (Zi Ton Dun: Yi Geng pairs -> Hour Geng Chen 07:00-09:00).
    # So Any Yi Day in Geng Year + Dragon Hour (07:00-09:00) gives 2 Geng.
    
    print("\nSearching for Female Case (Yi DM + 2 Geng Stems)...")
    start = datetime(1990, 1, 1)
    end = datetime(1990, 12, 31)
    curr = start
    while curr < end:
        solar = Solar.fromYmd(curr.year, curr.month, curr.day)
        lunar = solar.getLunar()
        y_gan = lunar.getYearInGanZhi()[0]
        d_gan = lunar.getDayInGanZhi()[0]
        
        if d_gan == '乙' and y_gan == '庚':
             print(f"FOUND Candidate: {curr.strftime('%Y-%m-%d')} (Yi Day in Geng Year)")
             print(f"Use Hour: 07:00-09:00 (Geng Chen Hour) -> Total 2 Geng (Year+Hour).")
             break
        curr += timedelta(days=1)

if __name__ == "__main__":
    find_dates()
