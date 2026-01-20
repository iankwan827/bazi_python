
import sys
import life_death_analysis

def run_debug():
    # Construct the chart based on User Case
    # Year: 壬申 (Ren Shen) - Owl / Owl Root
    # Month: 丙午 (Bing Wu) - Eating / Eating Root (Waittt, Wu doesn't have Bing. But Day has Yin!)
    # Day: 甲寅 (Jia Yin) - DM / Eating Root
    # Hour: 甲子 (Jia Zi) - Bi / Seal check
    
    pillars = [
        # Year
        {
            'gan': '壬', 'zhi': '申', 
            'tenGod': '偏印', # Full name likely from real app
            'hidden': [{'god': '七杀', 'stem': '庚'}, {'god': '偏印', 'stem': '壬'}, {'god': '偏财', 'stem': '戊'}] 
        },
        # Month
        {
            'gan': '丙', 'zhi': '午', 
            'tenGod': '食神', 
            'hidden': [{'god': '伤官', 'stem': '丁'}, {'god': '正财', 'stem': '己'}]
        },
        # Day
        {
            'gan': '甲', 'zhi': '寅', 
            'tenGod': '元男', 
            'hidden': [{'god': '比肩', 'stem': '甲'}, {'god': '食神', 'stem': '丙'}, {'god': '偏财', 'stem': '戊'}]
        },
        # Hour
        {
            'gan': '甲', 'zhi': '子', 
            'tenGod': '比肩', 
            'hidden': [{'god': '正印', 'stem': '癸'}]
        }
    ]
    
    print("Running check...")
    results = life_death_analysis.check_eating_god_meets_owl(pillars)
    print(f"Results Found: {len(results)}")
    for r in results:
        print(f"- {r['title']}")

    # Manual Debug of Logic Variables (Copy pasting logic snippet to see)
    stems_ten_gods = [p['tenGod'] for p in pillars]
    wealth_keywords = ['财', '才', '正财', '偏财']
    wealth_in_stems = any(any(kw in tg for kw in wealth_keywords) for tg in stems_ten_gods)
    print(f"Wealth In Stems: {wealth_in_stems}")
    
    eating_keywords = ['食', '食神']
    owl_keywords = ['枭', '偏印']
    
    def has_root(god_keywords, pillars):
        for p in pillars:
            for h in p['hidden']:
                if any(kw in h.get('god','') for kw in god_keywords): return True
        return False
        
    e_rooted = has_root(eating_keywords, pillars)
    o_rooted = has_root(owl_keywords, pillars)
    print(f"Eating Rooted: {e_rooted}")
    print(f"Owl Rooted: {o_rooted}")
    
    eating_indices = [i for i, x in enumerate(stems_ten_gods) if any(kw in x for kw in eating_keywords)]
    owl_indices = [i for i, x in enumerate(stems_ten_gods) if any(kw in x for kw in owl_keywords)]
    print(f"Eating Indices: {eating_indices}")
    print(f"Owl Indices: {owl_indices}")
    
if __name__ == "__main__":
    run_debug()
