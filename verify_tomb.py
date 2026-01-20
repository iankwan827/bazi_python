
import sys
import os

# Ensure we can import from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from bazi_logic import (
    get_all_earth_statuses, 
    GAN_WX, ZHI_WX, HIDDEN_STEMS_MAP, 
    calculate_body_strength
)

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

    # Case 6: Body Strength Phase 2 (Clash/Void Multiplier)
    print("\nCase 6: Body Strength Dynamic Correction")
    # DM: Jia (Wood). Month: Chen (Earth).
    # Earth consumes Wood. So Chen counts as 'Opposing Party' (Hao).
    # Wait, Chen (Earth) consumes Jia (Wood). Relation is 'Wealth' (Cai). Not 'Same Party'.
    # calculate_body_strength only adds score if 'Same Party'.
    # To test multiplier, we need Chen to be Same Party.
    # DM: Wu (Earth). Month: Chen (Earth). Same Party.
    
    # 6A: Closed Chen (No Clash). Multiplier 0.5.
    # Pillars: Wu Chen, Wu Yin, Wu Yin, Wu Yin. (No Xu).
    pillars6a = [
        {'gan': '戊', 'zhi': '辰'}, # Month (Index 1 usually, assuming pillars passed to strength are Y M D H)
        {'gan': '戊', 'zhi': '辰'}, # Wait, Month is Index 1.
        {'gan': '戊', 'zhi': '寅'}, # DM
        {'gan': '戊', 'zhi': '寅'}
    ]
    # Re-order to standard [Year, Month, Day, Hour]
    pillars_a = [
        {'gan': '戊', 'zhi': '寅'}, # Year
        {'gan': '戊', 'zhi': '辰'}, # Month (Earth - Same Party)
        {'gan': '戊', 'zhi': '寅'}, # Day
        {'gan': '戊', 'zhi': '寅'}  # Hour
    ]
    # Month Weight 45. Multiplier 0.5 (Closed). Exp: 22.5.
    str_a = calculate_body_strength(pillars_a)
    print(f"Strength A (Closed Chen): {str_a.get('total_score', str_a.get('score', 0))}") # Handle flexible return
    
    # 6B: Open Chen (Clashed by Xu). Multiplier 1.5 (Warehouse).
    # Need to ensure Chen is Warehouse.
    # Chen (Water Term). Roots? No. Stems? Need Stems.
    # Month Gan Wu (Earth). Not Water.
    # So Chen is Tomb?
    # Identity: P1 Root(No), P2 Stem(No). P3(No).
    # It's Tomb.
    # Tomb + Clash = Broken (0.2).
    # Let's make it Warehouse first. Add Ren (Water) stem.
    pillars_b = [
        {'gan': '戊', 'zhi': '戌'}, # Year (Clash Chen!)
        {'gan': '壬', 'zhi': '辰'}, # Month (Ren makes it Warehouse)
        {'gan': '戊', 'zhi': '寅'}, # Day
        {'gan': '戊', 'zhi': '寅'}  # Hour
    ]
    # Chen is Warehouse (Ren Stem). Clashed by Xu.
    # Multiplier 1.5. 
    # Month Weight 45 * 1.5 = 67.5.
    # Note: Ren stem is Water (Opposing).
    str_b = calculate_body_strength(pillars_b)
    print(f"Strength B (Open Warehouse Chen): {str_b.get('total_score', str_b.get('score', 0))}")
    
    score_a = str_a.get('total_score', str_a.get('score', 0))
    score_b = str_b.get('total_score', str_b.get('score', 0))
    
    assert score_b > score_a, f"Expected Open Warehouse ({score_b}) to provide more energy than Closed Branch ({score_a})"

    print("\nAll Tests Passed!")

if __name__ == "__main__":
    test_tomb_warehouse()
