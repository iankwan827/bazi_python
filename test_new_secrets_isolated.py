
from life_death_analysis import analyze_risks, get_future_risk_years

def test_secret_8():
    print("\n--- Testing Secret 8: 日支羊刃他处见 ---")
    # Case: Day Master 甲 (Jia), Day Branch 卯 (Mao) -> Yang Ren.
    # Other Yang Ren: Month Branch 卯.
    pillars = [
        {'gan': '丙', 'zhi': '寅', 'tenGod': '食神', 'hidden': []}, # Year
        {'gan': '丁', 'zhi': '卯', 'tenGod': '伤官', 'hidden': []}, # Month (Yang Ren!)
        {'gan': '甲', 'zhi': '卯', 'tenGod': '日主', 'hidden': []}, # Day (Yang Ren)
        {'gan': '戊', 'zhi': '辰', 'tenGod': '偏财', 'hidden': []}, # Hour
        {'gan': '己', 'zhi': '巳', 'tenGod': '正财', 'hidden': []}, # DY
        {'gan': '庚', 'zhi': '午', 'tenGod': '七杀', 'hidden': []}  # LN
    ]
    
    # Analyze
    risks = analyze_risks(pillars)
    found = False
    for r in risks:
        if "秘诀：日支羊刃他处见" in r['title']:
            print("MATCH FOUND!")
            print(f"Title: {r['title']}")
            print(f"Desc: {r['description']}")
            print(f"Trigger: {r['trigger_type']}")
            found = True
    if not found:
        print("NO MATCH FOUND (Unexpected)")

def test_secret_9():
    print("\n--- Testing Secret 9: 日坐羊刃逢冲 ---")
    # Case: Day Master 庚 (Geng), Day Branch 酉 (You) -> Yang Ren.
    # Da Yun: 卯 (Mao) -> Clashes You.
    
    base_pillars = [
        {'gan': '壬', 'zhi': '子', 'naYin': '桑柘木', 'tenGod': '', 'hidden': []}, # Year
        {'gan': '癸', 'zhi': '丑', 'naYin': '桑柘木', 'tenGod': '', 'hidden': []}, # Month
        {'gan': '庚', 'zhi': '酉', 'naYin': '石榴木', 'tenGod': '日主', 'hidden': []}, # Day (Yang Ren)
        {'gan': '甲', 'zhi': '申', 'naYin': '泉中水', 'tenGod': '', 'hidden': []}  # Hour
    ]
    
    da_yun_list = [
        {
            'ganZhi': '乙卯', 'gan': '乙', 'zhi': '卯', 'tenGod': '正财', 'naYin': '大溪水',
            'liuNian': [
                {'ganZhi': '丙辰', 'gan': '丙', 'zhi': '辰', 'tenGod': '七杀', 'year': 2024, 'naYin': '沙中土'}
            ]
        }
    ]
    
    data = {
        'pillars': base_pillars,
        'daYunList': da_yun_list
    }
    
    forecast = get_future_risk_years(data)
    found = False
    for f in forecast:
        if "秘诀：配偶血光" in f['risk']:
            print("MATCH FOUND!")
            print(f"Year: {f['year']}")
            print(f"Risk: {f['risk']}")
            print(f"Desc: {f['desc']}")
            print(f"Trigger: {f['trigger_type']}")
            found = True
            
    if not found:
        print("NO MATCH FOUND (Unexpected)")

if __name__ == "__main__":
    test_secret_8()
    test_secret_9()
