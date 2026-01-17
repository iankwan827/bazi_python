import sys
import os

# Ensure we can import bazi_logic
sys.path.append(os.getcwd())
try:
    from bazi_logic import get_interactions
except ImportError:
    # Try parent directory if running from subdirectory
    sys.path.append(os.path.dirname(os.getcwd()))
    from bazi_logic import get_interactions

def test_relations():
    # Helper to create dummy pillars
    def make_pillars(zhis):
        return [{'gan': '甲', 'zhi': z} for z in zhis]

    tests = [
        # San Hui
        (['寅', '卯', '辰'], '寅卯辰三会木方'),
        (['巳', '午', '未'], '巳午未三会火方'),
        (['申', '酉', '戌'], '申酉戌三会金方'),
        (['亥', '子', '丑'], '亥子丑三会水方'),

        # Ban He
        (['申', '子'], '申子半合(水局)'),
        (['子', '辰'], '子辰半合(水局)'),
        (['亥', '卯'], '亥卯半合(木局)'),
        (['卯', '未'], '卯未半合(木局)'),
        (['寅', '午'], '寅午半合(火局)'),
        (['午', '戌'], '午戌半合(火局)'),
        (['巳', '酉'], '巳酉半合(金局)'),
        (['酉', '丑'], '酉丑半合(金局)'),

        # An He (User requested specific additions, now Dynamic)
        # Zi (Gui) - Si (Bing, Geng, Wu) -> Gui-Wu He (Fire)
        (['子', '巳'], '子巳暗合'),
        
        # Yin (Jia, Bing, Wu) - Wei (Ji, Ding, Yi) -> Jia-Ji, Bing-Xin(No), Wu-Gui(No) -> Jia-Ji He (Earth)
        (['寅', '未'], '寅未暗合'),
        
        # Test a standard one too: Yin (Jia, Bing, Wu) - Chou (Ji, Gui, Xin) -> Jia-Ji He, Bing-Xin He
        (['寅', '丑'], '寅丑暗合'),
        
        # Mixed / Multiple
        (['申', '子', '辰'], '申子半合(水局)'), # Should find Ban He pairs too? 
                                          # Logic adds pairs pairwise. 
                                          # Shen-Zi-Chen is also San He '申子辰三合水局'.
                                          # Code has both logic now.
    ]

    failed = 0
    for zhis, expected in tests:
        pillars = make_pillars(zhis)
        result = get_interactions(pillars)
        branches_res = result['branches']
        
        found = False
        for item in branches_res:
             if expected in item:
                 found = True
                 break
        
        if found:
            print(f"[PASS] {zhis} -> Found {expected}")
        else:
            print(f"[FAIL] {zhis} -> Expected {expected}, Got {branches_res}")
            failed += 1

    # Check San Xing Name Update and Order Independence
    # Test 1: Standard Order
    pillars = make_pillars(['丑', '未', '戌'])
    res = get_interactions(pillars)['branches']
    if '丑未戌三刑' in res:
        print("[PASS] 丑未戌三刑 (Standard Order) detected")
    else:
        print(f"[FAIL] 丑未戌三刑 (Standard Order) NOT detected, got: {res}")
        failed += 1

    # Test 2: Scrambled Order
    pillars_scrambled = make_pillars(['戌', '丑', '未'])
    res_scrambled = get_interactions(pillars_scrambled)['branches']
    if '丑未戌三刑' in res_scrambled:
        print("[PASS] 丑未戌三刑 (Scrambled Order '戌, 丑, 未') detected")
    else:
        print(f"[FAIL] 丑未戌三刑 (Scrambled Order) NOT detected, got: {res_scrambled}")
        failed += 1
        
    # Test 3: Standard Order Yin-Si-Shen
    pillars_yss = make_pillars(['寅', '巳', '申'])
    res_yss = get_interactions(pillars_yss)['branches']
    if '寅巳申三刑' in res_yss:
        print("[PASS] 寅巳申三刑 (Standard Order) detected")
    else:
        failed += 1
        
    # Test 4: Scrambled Order Yin-Si-Shen
    pillars_yss_scrambled = make_pillars(['申', '寅', '巳'])
    res_yss_scrambled = get_interactions(pillars_yss_scrambled)['branches']
    if '寅巳申三刑' in res_yss_scrambled:
        print("[PASS] 寅巳申三刑 (Scrambled Order '申, 寅, 巳') detected")
    else:
        print(f"[FAIL] 寅巳申三刑 (Scrambled Order) NOT detected, got: {res_yss_scrambled}")
        failed += 1

    if failed == 0:
        print("\nAll tests passed!")
    else:
        print(f"\n{failed} tests failed.")

if __name__ == "__main__":
    test_relations()
