
import datetime
from lunar_python import Solar
from bazi_logic import HIDDEN_STEMS_MAP, TEN_GODS
import sys
import io

# Force utf-8 stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_ten_god(day_gan, target_gan):
    key = day_gan + target_gan
    val = TEN_GODS.get(key)
    return val[0] if val else ''

def inspect_date(date_str):
    print(f"--- Inspecting {date_str} ---")
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    solar = Solar.fromYmdHms(dt.year, dt.month, dt.day, 12, 0, 0)
    lunar = solar.getLunar()
    bazi = lunar.getEightChar()
    
    yg = bazi.getYearGan()
    yz = bazi.getYearZhi()
    mg = bazi.getMonthGan()
    mz = bazi.getMonthZhi()
    dg = bazi.getDayGan()
    dz = bazi.getDayZhi()
    hg = bazi.getTimeGan()
    hz = bazi.getTimeZhi()
    
    print(f"Date: {date_str}")
    print(f"Pillars (GanZhi): Y={yg}{yz} M={mg}{mz} D={dg}{dz} H={hg}{hz}")
    print(f"Day Master: {dg}")
    
    # Check Year Branch Main Qi
    y_hidden = HIDDEN_STEMS_MAP.get(yz, [])
    y_main = y_hidden[0] if y_hidden else ''
    y_tg = get_ten_god(dg, y_main)
    print(f"Year Branch {yz} MainQi: {y_main} -> TenGod: {y_tg}")
    
    # Check Month Branch Main Qi
    m_hidden = HIDDEN_STEMS_MAP.get(mz, [])
    m_main = m_hidden[0] if m_hidden else ''
    m_tg = get_ten_god(dg, m_main)
    print(f"Month Branch {mz} MainQi: {m_main} -> TenGod: {m_tg}")

if __name__ == '__main__':
    inspect_date("1980-01-06")
