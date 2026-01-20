
import datetime
from lunar_python import Solar
from bazi_logic import HIDDEN_STEMS_MAP, TEN_GODS
import sys

# Pinyin Maps
GAN_PY = {
    '甲': 'Jia', '乙': 'Yi', '丙': 'Bing', '丁': 'Ding', '戊': 'Wu',
    '己': 'Ji', '庚': 'Geng', '辛': 'Xin', '壬': 'Ren', '癸': 'Gui'
}
ZHI_PY = {
    '子': 'Zi', '丑': 'Chou', '寅': 'Yin', '卯': 'Mao', '辰': 'Chen', '巳': 'Si',
    '午': 'Wu', '未': 'Wei', '申': 'Shen', '酉': 'You', '戌': 'Xu', '亥': 'Hai'
}
TG_PY = {
    '比肩': 'BiJian', '比': 'Bi',
    '劫财': 'JieCai', '劫': 'Jie',
    '食神': 'ShiShen', '食': 'Shi',
    '伤官': 'ShangGuan', '伤': 'Shang',
    '偏财': 'PianCai', '才': 'Cai',
    '正财': 'ZhengCai', '财': 'ZhengCai', # Map short '财' to ZhengCai
    '七杀': 'QiSha', '杀': 'Sha',
    '正官': 'ZhengGuan', '官': 'Guan',
    '偏印': 'PianYin', '枭': 'Xiao',
    '正印': 'ZhengYin', '印': 'Yin'
}

def get_ten_god(day_gan, target_gan):
    key = day_gan + target_gan
    val = TEN_GODS.get(key)
    # Return Pinyin of Full Name
    if val:
        return TG_PY.get(val[0], val[0]) 
    return 'None'

def to_py(char):
    if char in GAN_PY: return GAN_PY[char]
    if char in ZHI_PY: return ZHI_PY[char]
    return char

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
    
    print(f"Pillars: Y={to_py(yg)}{to_py(yz)} M={to_py(mg)}{to_py(mz)} D={to_py(dg)}{to_py(dz)}")
    print(f"Day Master: {to_py(dg)}")
    
    # Year Branch
    y_hidden = HIDDEN_STEMS_MAP.get(yz, [])
    if y_hidden:
        y_main = y_hidden[0]
        y_god = get_ten_god(dg, y_main)
        print(f"Year Branch {to_py(yz)} MainQi: {to_py(y_main)} -> TenGod: {y_god}")
    else:
        print(f"Year Branch {to_py(yz)} No Hidden")

    # Month Branch
    m_hidden = HIDDEN_STEMS_MAP.get(mz, [])
    if m_hidden:
        m_main = m_hidden[0]
        m_god = get_ten_god(dg, m_main)
        print(f"Month Branch {to_py(mz)} MainQi: {to_py(m_main)} -> TenGod: {m_god}")
    else:
        print(f"Month Branch {to_py(mz)} No Hidden")

if __name__ == '__main__':
    inspect_date("1980-01-12")
