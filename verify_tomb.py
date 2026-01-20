
import sys
import os

# Ensure we can import from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bazi_logic import get_tomb_warehouse_status

def test_tomb_warehouse():
    print("Testing Tomb/Warehouse Logic...")
    
    # Setup Mock Pillars (Simple structure compatible with function)
    # Pillars: [Year, Month, Day, Hour]
    
    # Case 1: Chen Warehouse (High Score + Revealed Target)
    print("\nCase 1: Chen (Water) - High Score (30%) + Ren (Water) Stem")
    pillars1 = [
        {'gan': '壬', 'zhi': '辰'}, # Year: Ren (Water) Chen
        {'gan': '甲', 'zhi': '寅'},
        {'gan': '丙', 'zhi': '午'},
        {'gan': '戊', 'zhi': '子'}
    ]
    scores1 = {'水': 30, '木': 20, '火': 20, '土': 20, '金': 10} # Total 100
    res1 = get_tomb_warehouse_status(pillars1, scores1)
    print(f"Result: {res1.get(0)}")
    assert res1[0]['type'] == 'Warehouse', "Expected Warehouse for Chen with High Water & Ren Stem"

    # Case 2: Chen Tomb (Low Score)
    print("\nCase 2: Chen (Water) - Low Score (10%) + Ren Stem")
    scores2 = {'水': 10, '木': 30, '火': 30, '土': 20, '金': 10} # Total 100
    res2 = get_tomb_warehouse_status(pillars1, scores2) # Using pillars1 (Ren Stem present)
    print(f"Result: {res2.get(0)}")
    assert res2[0]['type'] == 'Tomb', "Expected Tomb for Chen with Low Water Score"

    # Case 3: Chen Tomb (High Score but No Stem)
    print("\nCase 3: Chen (Water) - High Score (30%) + No Water/Metal Stem")
    pillars3 = [
        {'gan': '甲', 'zhi': '辰'}, # Year: Jia (Wood) Chen
        {'gan': '丙', 'zhi': '寅'},
        {'gan': '戊', 'zhi': '午'},
        {'gan': '己', 'zhi': '丑'}
    ]
    # Stems: Wood, Fire, Earth, Earth. No Water (Target) or Metal (Source).
    res3 = get_tomb_warehouse_status(pillars3, scores1) # Scores1 has high Water
    print(f"Result: {res3.get(0)}")
    assert res3[0]['type'] == 'Tomb', "Expected Tomb for Chen with High Score but No Revealed Stem"

    # Case 4: Xu Warehouse (High Score + Producing Stem)
    print("\nCase 4: Xu (Fire) - High Score (30%) + Jia (Wood) Stem (Producing)")
    pillars4 = [
        {'gan': '甲', 'zhi': '戌'}, # Year: Jia (Wood) Xu. Jia produces Fire.
        {'gan': '丙', 'zhi': '寅'},
        {'gan': '戊', 'zhi': '午'},
        {'gan': '己', 'zhi': '丑'}
    ]
    scores4 = {'火': 30, '木': 20, '土': 20, '金': 20, '水': 10}
    res4 = get_tomb_warehouse_status(pillars4, scores4)
    print(f"Result: {res4.get(0)}")
    assert res4[0]['type'] == 'Warehouse', "Expected Warehouse for Xu with High Fire & producing Wood Stem"

    print("\nAll Tests Passed!")

if __name__ == "__main__":
    test_tomb_warehouse()
