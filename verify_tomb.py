
import sys
import os

# Ensure we can import from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from bazi_logic import get_all_earth_statuses

def test_tomb_warehouse():
    print("Testing Tomb/Warehouse Logic (All 4)...")
    
    # Case 1: Chen Warehouse environment
    print("\nCase 1: Environment with High Water + Ren Stem")
    pillars1 = [
        {'gan': '壬', 'zhi': '子'}, # Ren Stem, doesn't matter what branch
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '丙', 'zhi': '午'},
        {'gan': '戊', 'zhi': '子'}
    ]
    scores1 = {'水': 30, '木': 20, '火': 20, '土': 20, '金': 10} 
    res1 = get_all_earth_statuses(pillars1, scores1)
    
    print(f"Result for Chen: {res1.get('辰')}")
    assert res1['辰']['type'] == 'Warehouse', "Expected Warehouse for Chen"
    
    print(f"Result for Xu: {res1.get('戌')}")
    # Xu (Fire). Roots: Si, Wu. Pillars: [Zi, Yin, Wu, Zi].
    # Wu (Day Branch) is Fire. Has Root!
    # Stems: Ren, Jia, Bing, Wu. Bing (Fire) is Revealed.
    # Root + Revealed -> Warehouse.
    # Previous check failed because Score < 20% (Low Fire).
    # New Check: Has Root (Wu) OR Revealed (Bing) -> Warehouse.
    assert res1['戌']['type'] == 'Warehouse', "Expected Warehouse for Xu (Has Root 'Wu' + Revealed 'Bing')"

    # Case 2: Only Stem Revealed (No Root) -> Previous Floating Case
    print("\nCase 2: Stem Revealed but No Root")
    # Pillars: [Jia Chen, ..., ..., ...]
    # Suppose Chen(Water). No Zi/Hai. But Stem Ren(Water) exists.
    # Pillars: Ren Chen, Jia Yin, Jia Yin, Jia Yin.
    pillars2 = [
        {'gan': '壬', 'zhi': '辰'}, 
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '甲', 'zhi': '寅'}
    ]
    scores2 = {} # Ignored
    res2 = get_all_earth_statuses(pillars2, scores2)
    # Chen (Water). Root: None (Yin/Chen are Wood/Earth).
    # Stem: Ren (Water). Revealed.
    # Logic: Revealed OR Root -> Warehouse.
    print(f"Result for Chen: {res2.get('辰')}")
    assert res2['辰']['type'] == 'Warehouse', "Expected Warehouse for Chen (Stem Revealed)"

    # Case 3: Only Root (No Stem)
    print("\nCase 3: Root Exists but No Stem")
    # Pillars: Jia Zi, ..., ..., ...
    # Chen(Water). Root: Zi (Water). Stem: Jia (Wood). Not Revealed.
    pillars3 = [
        {'gan': '甲', 'zhi': '子'},
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '甲', 'zhi': '寅'}
    ]
    res3 = get_all_earth_statuses(pillars3, {})
    # Chen(Water). Root: Zi (Yes).
    # Logic: Root OR Revealed -> Warehouse.
    print(f"Result for Chen: {res3.get('辰')}")
    assert res3['辰']['type'] == 'Warehouse', "Expected Warehouse for Chen (Root Exists)"

    # Case 4: Pure Tomb (No Root, No Stem)
    print("\nCase 4: Pure Tomb")
    # Pillars: Jia Chen, ...
    # No Water Root, No Water Stem.
    pillars4 = [
        {'gan': '甲', 'zhi': '辰'},
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '甲', 'zhi': '寅'}
    ]
    res4 = get_all_earth_statuses(pillars4, {})
    print(f"Result for Chen: {res4.get('辰')}")
    assert res4['辰']['type'] == 'Tomb', "Expected Tomb for Chen (No Root, No Stem)"

    print("\nAll Tests Passed!")

if __name__ == "__main__":
    test_tomb_warehouse()
