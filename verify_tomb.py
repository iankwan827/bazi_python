
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
    # Xu (Fire). Roots: Wu (+30). Revealed Bing (+15). Hidden Ding in Xu (+8).
    # Total Unreduced > 12.
    assert res1['戌']['type'] == 'Warehouse', "Expected Warehouse for Xu (Strong)"

    # Case 2: Only Stem Revealed (No Root)
    print("\nCase 2: Stem Revealed but No Root")
    # Pillars: Ren Chen (Stem +15, Hidden +8 = 23).
    pillars2 = [
        {'gan': '壬', 'zhi': '辰'}, 
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '甲', 'zhi': '寅'}
    ]
    res2 = get_all_earth_statuses(pillars2, {})
    # Score: Stem Ren(15) + Hidden Gui in Chen(8) = 23. > 12.
    print(f"Result for Chen: {res2.get('辰')}")
    assert res2['辰']['type'] == 'Warehouse', "Expected Warehouse for Chen (Stem Revealed)"

    # Case 3: Only Root (No Stem)
    print("\nCase 3: Root Exists but No Stem")
    # Pillars: Jia Zi (Root +30) + Chen (Hidden +8).
    pillars3 = [
        {'gan': '甲', 'zhi': '子'},
        {'gan': '甲', 'zhi': '辰'},
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '甲', 'zhi': '寅'}
    ]
    res3 = get_all_earth_statuses(pillars3, {})
    # Score: Zi(30) + Chen_Hidden(8) = 38. > 12.
    print(f"Result for Chen: {res3.get('辰')}")
    assert res3['辰']['type'] == 'Warehouse', "Expected Warehouse for Chen (Root Exists)"

    # Case 4: Pure Tomb (No Root, No Stem, Single Tomb)
    print("\nCase 4: Pure Tomb")
    # Pillars: Jia Chen. 
    # Score: Hidden Gui in Chen(8). < 12.
    pillars4 = [
        {'gan': '甲', 'zhi': '辰'},
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '甲', 'zhi': '寅'}
    ]
    res4 = get_all_earth_statuses(pillars4, {})
    print(f"Result for Chen: {res4.get('辰')}")
    assert res4['辰']['type'] == 'Tomb', "Expected Tomb for Chen (Single Tomb < Threshold)"

    # Case 5: Two Tombs (Accumulation)
    print("\nCase 5: Two Tombs")
    # Pillars: Jia Chen, Jia Chen.
    # Score: Hidden(8) + Hidden(8) = 16. > 12.
    pillars5 = [
        {'gan': '甲', 'zhi': '辰'},
        {'gan': '甲', 'zhi': '辰'},
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '甲', 'zhi': '寅'}
    ]
    res5 = get_all_earth_statuses(pillars5, {})
    print(f"Result for Chen: {res5.get('辰')}")
    assert res5['辰']['type'] == 'Warehouse', "Expected Warehouse for 2x Chen (Accumulation > Threshold)"

    print("\nAll Tests Passed!")

if __name__ == "__main__":
    test_tomb_warehouse()
