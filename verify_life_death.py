
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import life_death_analysis

def verify_detailed_rules():
    print("Verifying Detailed 'Eating God Meets Owl' Rules...")
    
    # ---------------------------------------------------------
    # Scenario: Luck Cycle (Da Yun) and Annual Pillar (Liu Nian)
    # ---------------------------------------------------------
    print("\n[Scenario: Luck Cycle & Annual Pillar Verification]")
    
    # Base Chart: 
    # Day Master: 甲 (Jia Wood)
    # Year: 乙亥 (Rob Wealth / Owl) -> Hai contains Ren(Owl). But let's keep it simple first.
    # Let's make a Base Chart that is "Clean" (No Eating God Meets Owl).
    # Month: 丙寅 (Eating God / Bi).
    # Day: 甲子 (DM / Seal).
    # Hour: 戊辰 (Wealth / Wealth). -> Wealth prevents Adjacency issue if stems are adjacent.
    # But wait, we want to test "Triggering" it.
    
    # Let's try to construct the user's specific case:
    # "If original doesn't constitute, then look at flow..."
    
    # Base Chart (Safe)
    # DM: 甲 (Jia)
    # Year: 辛酉 (Officer)
    # Month: 庚寅 (Kill / Bi) -> Yin contains Bing(Eating), Jia(Bi), Wu(Wealth).
    # Day: 甲戌 (DM / Wealth) -> Xu contains Wu, Xin, Ding(Shang).
    # Hour: 乙亥 (Rob / Owl) -> Hai contains Ren(Owl), Jia.
    #
    # Analysis:
    # Stems: Xin, Geng, Jia, Yi. -> No Eating God (Bing) or Owl (Ren) in Stems.
    # Branches: 
    #   Yin (Eating God 'Bing' inside).
    #   Hai (Owl 'Ren' inside).
    # Interaction: Yin-Hai is Six Harmony (He).
    # Does Six Harmony count? 
    # Code says: '六合' is in the interaction list.
    # So this Base Chart might ALREADY trigger Rule 4 (Interaction).
    # Let's choose branches that don't interact.
    # Yin (Eating) and Zi (Owl). Zi-Yin is not standard interaction (maybe nothing).
    
    print("\n--- Step 1: Base Chart (Clean) ---")
    base_chart = [
        {'gan': '辛', 'zhi': '卯', 'tenGod': '官', 'hidden': [{'god': '劫'}]}, # Year
        {'gan': '庚', 'zhi': '寅', 'tenGod': '杀', 'hidden': [{'god': '比'}, {'god': '食'}, {'god': '才'}]}, # Month (Has Eating)
        {'gan': '甲', 'zhi': '辰', 'tenGod': '元男', 'hidden': []}, # Day
        {'gan': '乙', 'zhi': '丑', 'tenGod': '劫', 'hidden': []}  # Hour (Clean)
    ] 
    # Check Base
    # Owl? No Owl in Stems. No Owl in Branches (Mao, Yin, Chen, Chou).
    # Wait, Chou contains Gui (Seal), Xin (Officer), Ji (Wealth). Gui is Zheng Yin (Seal), not Xiao (Owl).
    # So Base Chart has NO Owl. -> Safe.
    check(base_chart, "Base Chart (Should be Safe)", expect=False)
    
    
    print("\n--- Step 2: Add Da Yun (Trigger via Non-Adjacent Stem) ---")
    # Da Yun: 壬 (Owl).
    # Original Chart: Year has Eating God. Hour is safe.
    # Year: Bing (Eating). 
    # Da Yun: Ren (Owl).
    # Indices: 0 (Year) and 4 (Da Yun). Distance = 4. NOT adjacent.
    # Should still trigger because Da Yun doesn't need adjacency.
    
    base_chart_non_adj = [
        {'gan': '丙', 'zhi': '寅', 'tenGod': '食', 'hidden': [{'god': '食'}]},  # Year: Eating, Rooted
        {'gan': '庚', 'zhi': '寅', 'tenGod': '杀', 'hidden': []}, 
        {'gan': '甲', 'zhi': '辰', 'tenGod': '元男', 'hidden': []}, 
        {'gan': '乙', 'zhi': '丑', 'tenGod': '劫', 'hidden': []}
    ]
    # Add Da Yun: Ren (Owl). Rooted in Wu (contains Ji/Ding, but let's add Owl for test) 
    # Or just say Da Yun ZHI is rooted by Year/etc.
    # But rule is "Root in ANY branch".
    # Let's say Da Yun Branch 'Wu' has Owl. (Not true for Wu, but for test sake).
    # Or better: Da Yun is Ren-Shen (Owl-Owl). 
    da_yun = {'gan': '壬', 'zhi': '申', 'tenGod': '枭', 'hidden': [{'god': '枭'}]}
    
    pillars_with_dayun = base_chart_non_adj + [da_yun]
    # Check: Year(Bing) vs DaYun(Ren).
    check(pillars_with_dayun, "Da Yun Stem Non-Adjacent (Bing-Ren)", expect=True)


    print("\n--- Step 3: Add Liu Nian (Trigger via Branch Interaction) ---")
    # Base Chart 3:
    # DM: 甲. 
    # Chart has Eating God in Branch: 巳 (Si) -> Contains Bing (Eating).
    base_chart_3 = [
        {'gan': '甲', 'zhi': '子', 'tenGod': '比', 'hidden': [{'god': '印'}]}, # Year
        {'gan': '甲', 'zhi': '子', 'tenGod': '比', 'hidden': [{'god': '印'}]}, # Month
        {'gan': '甲', 'zhi': '子', 'tenGod': '元男', 'hidden': [{'god': '印'}]}, # Day
        {'gan': '己', 'zhi': '巳', 'tenGod': '财', 'hidden': [{'god': '食'}, {'god': '杀'}, {'god': '才'}]} # Hour: Si (Has Eating)
    ]
    # Da Yun: Neutral.
    da_yun = {'gan': '甲', 'zhi': '子', 'tenGod': '比', 'hidden': []}
    
    # Liu Nian: 亥 (Hai). Contains Ren (Owl).
    # Hai clashes with Si (Hour Branch).
    liu_nian = {'gan': '乙', 'zhi': '亥', 'tenGod': '劫', 'hidden': [{'god': '枭'}, {'god': '比'}]}
    
    pillars_full = base_chart_3 + [da_yun, liu_nian]
    
    check(pillars_full, "Liu Nian Branch Interaction (Si-Hai Clash)", expect=True)

    print("\n--- Step 4: Sui Yun Bing Lin (Year matches Luck) ---")
    # Da Yun: Ren Wu
    dy_sybl = {'gan': '壬', 'zhi': '午', 'tenGod': '枭', 'hidden': []}
    # Liu Nian: Ren Wu (Same)
    ln_sybl = {'gan': '壬', 'zhi': '午', 'tenGod': '枭', 'hidden': []}
    
    pillars_sybl = base_chart_3 + [dy_sybl, ln_sybl]
    check(pillars_sybl, "Sui Yun Bing Lin", expect=True)

    print("\n--- Step 5: Three Clashes One (3 vs 1) ---")
    # Base: Year=Zi, Month=Zi, Day=Zi. (3 Zis). Target=Wu.
    # Da Yun = Wu.
    # Checks: 3 Zi in Original vs 1 Wu in Da Yun? 
    # Rule says: "3 identical branches clash with 1 branch in ORIGINAL".
    # So the 1 Target MUST be in Original.
    # The 3 Attackers can be anywhere.
    
    # Case: Year=Zi, Month=Zi. (2 Zis). Hour=Wu (Target).
    # Da Yun = Zi. -> Total 3 Zis. Target Wu is in Hour. -> Trigger.
    base_tco = [
        {'gan': '甲', 'zhi': '子', 'tenGod': '比', 'hidden': []},
        {'gan': '甲', 'zhi': '子', 'tenGod': '比', 'hidden': []},
        {'gan': '甲', 'zhi': '辰', 'tenGod': '元', 'hidden': []},
        {'gan': '甲', 'zhi': '午', 'tenGod': '财', 'hidden': []} # Target Wu
    ]
    dy_tco = {'gan': '甲', 'zhi': '子', 'tenGod': '比', 'hidden': []} # 3rd Zi
    ln_tco = {'gan': '甲', 'zhi': '丑', 'tenGod': '官', 'hidden': []} # Neutral
    
    p_tco = base_tco + [dy_tco, ln_tco]
    check(p_tco, "Three Clashes One (3 Zi vs 1 Wu)", expect=True)

    print("\n--- Step 6: Fan Yin Fu Yin (Reverse/Hidden Chant) ---")
    # Base: Day = Jia Zi (甲子)
    base_fy = [
        {'gan': '甲', 'zhi': '寅', 'tenGod': '比', 'hidden': []},
        {'gan': '丙', 'zhi': '寅', 'tenGod': '食', 'hidden': []},
        {'gan': '甲', 'zhi': '子', 'tenGod': '元', 'hidden': []}, # Day: Jia Zi
        {'gan': '乙', 'zhi': '丑', 'tenGod': '劫', 'hidden': []}
    ]
    
    # Case 1: Fu Yin (Da Yun = Jia Zi)
    dy_fu = {'gan': '甲', 'zhi': '子', 'tenGod': '比', 'hidden': []}
    ln_neutral = {'gan': '丙', 'zhi': '辰', 'tenGod': '食', 'hidden': []}
    check(base_fy + [dy_fu, ln_neutral], "Fu Yin (Da Yun == Day)", expect=True)
    
    # Case 2: Fan Yin (Liu Nian = Geng Wu)
    # Jia vs Geng (Tian Ke, 7th). Zi vs Wu (Di Chong).
    dy_neutral = {'gan': '丙', 'zhi': '辰', 'tenGod': '食', 'hidden': []}
    ln_fan = {'gan': '庚', 'zhi': '午', 'tenGod': '杀', 'hidden': []}
    check(base_fy + [dy_neutral, ln_fan], "Fan Yin (Liu Nian Geng-Wu vs Day Jia-Zi)", expect=True)
    
def check(pillars, name, expect=True):
    res = life_death_analysis.check_eating_god_meets_owl(pillars)
    found = len(res) > 0
    status = "PASS" if found == expect else "FAIL"
    print(f"  - {name}: {status} (Expected {expect}, Got {found})")
    if found:
        for r in res:
             print(f"    * Detected: {r['title']} - {r['description']}")

if __name__ == "__main__":
    verify_detailed_rules()
