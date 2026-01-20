
import datetime
from lunar_python import Solar
from bazi_logic import calculate_bazi, calculate_body_strength, calculate_yong_xi_ji, calculate_global_scores

def run_debug():
    # 1996-3-22 8:00
    dt_obj = datetime.datetime(1996, 3, 22, 8, 0)
    print(f"Debug Date: {dt_obj}")
    
    # calculate_bazi takes (date, gender)
    bazi_result = calculate_bazi(dt_obj, 'M') 
    pillars = bazi_result['pillars']
    print("Pillars:", [p['gan'] + p['zhi'] for p in pillars])
    
    # Calculate Body Strength (Original 4 pillars)
    bs = calculate_body_strength(pillars)
    print("\n--- Body Strength Result ---")
    print(f"Body Strength Keys: {list(bs.keys())}")
    print(f"Level: {bs.get('level')}")
    # print(f"Total Score: {bs.get('total_score')}") 
    print(f"Is Guan Yin: {bs.get('isGuanYin')}")
    
    # Calculate Yong Xi Ji
    result = calculate_yong_xi_ji(pillars, bs)
    print("\n--- Yong Xi Ji Result ---")
    print(f"Yong: {result.get('yong')}")
    print(f"Xi: {result.get('xi')}")
    print(f"Ji: {result.get('ji')}")
    print(f"Reason: {result.get('reason')}")
    
    # Analyze Scores for trigger
    print("\n--- Score Analysis ---")
    scores = calculate_global_scores(pillars)
    print("Scores Dict:", scores)
    
    dm_wx = '土' # We know it's Wu Earth
    seal = '火'
    same = '土'
    
    seal_score = scores.get(seal, 0)
    same_score = scores.get(same, 0)
    group_a = seal_score + same_score
    ratio = seal_score / group_a if group_a > 0 else 0
    
    print(f"Seal (Fire): {seal_score}")
    print(f"Same (Earth): {same_score}")
    print(f"Group A (Seal+Same): {group_a}")
    print(f"Seal Ratio: {ratio:.2f}")
    print(f"Trigger Thresholds: GroupA > 52 AND Ratio > 0.7")
    
    # Season Check
    mz = pillars[1]['zhi']
    # Need ZHI_WX and WX_RELATION mappings which are local to logic file or need import. Only 1996 case needed here.
    # WX_RELATION copied for debug or imported? Hardcode for this case.
    # Month is Mao (Wood). Seal is Fire.
    mz_wx = '木' 
    seal = '火'
    season_supports = True # Wood generates Fire
    
    print(f"Season Supports? {season_supports} (Month {mz} grows Seal {seal})")
    print(f"Is Triggered (Old)? {group_a > 52 and ratio > 0.7}")
    print(f"Is Triggered (New)? {group_a > 52 and (ratio > 0.7 or (ratio > 0.6 and season_supports))}")

if __name__ == "__main__":
    run_debug()
