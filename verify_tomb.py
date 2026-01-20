
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
    # Fire score is 20 (Total 100) -> 20%. Not > 20%. So Tomb.
    # Wait, 20/100 is not > 0.20. It's ==. Logic says > 0.20.
    assert res1['戌']['type'] == 'Tomb', "Expected Tomb for Xu (Score not > 20%)"

    # Case 2: High Fire Score for Xu
    print("\nCase 2: Environment with High Fire + No Producing Stem")
    scores2 = {'水': 10, '木': 10, '火': 40, '土': 20, '金': 20}
    # Stems in pillars1: Ren(Water), Jia(Wood), Bing(Fire), Wu(Earth).
    # For Xu (Fire), Target is Fire. Producing is Wood.
    # Pillars have Jia (Wood) and Bing (Fire).
    # So both Cond A (>20%) and Cond B (Stem Revealed) should be Met.
    res2 = get_all_earth_statuses(pillars1, scores2)
    print(f"Result for Xu: {res2.get('戌')}")
    assert res2['戌']['type'] == 'Warehouse', "Expected Warehouse for Xu"

    print("\nAll Tests Passed!")

if __name__ == "__main__":
    test_tomb_warehouse()
