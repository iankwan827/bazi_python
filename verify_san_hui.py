
from bazi_logic import get_dynamic_interactions

def verify():
    # Construct pillars: Year(申), Month(酉), Day(子), Hour(丑)
    # Dynamic: Da Yun(戌), Liu Nian(亥)
    pillars = [
        {'gan': '甲', 'zhi': '申'}, # Year
        {'gan': '乙', 'zhi': '酉'}, # Month
        {'gan': '丙', 'zhi': '子'}, # Day
        {'gan': '丁', 'zhi': '丑'}, # Hour
        {'gan': '戊', 'zhi': '戌'}, # Da Yun (Dynamic)
        {'gan': '己', 'zhi': '亥'}  # Liu Nian (Dynamic)
    ]
    
    # Dynamic indices for Da Yun (4) and Liu Nian (5)
    dynamic_indices = [4, 5]
    
    result = get_dynamic_interactions(pillars, dynamic_indices)
    
    print("Combined Branches:", [p['zhi'] for p in pillars])
    print("Result Branches:", result['branches'])
    
    if "申酉戌三会金方" in result['branches']:
        print("SUCCESS: 申酉戌三会金方 found!")
    else:
        print("FAILURE: 申酉戌三会金方 NOT found.")

if __name__ == "__main__":
    verify()
