
import datetime
from lunar_python import Solar
from bazi_logic import HIDDEN_STEMS_MAP, TEN_GODS

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
    
    print(f"Pillars: {yg}{yz}  {mg}{mz}  {dg}{dz}")
    
    # Check Ten Gods for Year/Month Branch Main Qi
    y_hidden_stems = HIDDEN_STEMS_MAP.get(yz, [])
    m_hidden_stems = HIDDEN_STEMS_MAP.get(mz, [])
    
    print(f"Year Branch {yz} Hidden Stems: {y_hidden_stems}")
    print(f"Month Branch {mz} Hidden Stems: {m_hidden_stems}")
    
    if y_hidden_stems:
        y_main = y_hidden_stems[0]
        y_god = get_ten_god(dg, y_main)
        print(f"Year Main Qi: {y_main} -> Ten God: {y_god}")
        
    if m_hidden_stems:
        m_main = m_hidden_stems[0]
        m_god = get_ten_god(dg, m_main)
        print(f"Month Main Qi: {m_main} -> Ten God: {m_god}")

if __name__ == '__main__':
    inspect_date("1980-01-06")
