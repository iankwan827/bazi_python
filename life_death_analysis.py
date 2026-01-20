
"""
Life and Death Analysis Module for Bazi.

This module contains rules and logic for determining potential life-threatening situations
based on Bazi charts.

Reference: 死亡断事三板斧.md
"""

# Global Mapping
GAN_WX = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}
ZHI_WX = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
    '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'
}
GAN_HE = {
    '甲': '己', '乙': '庚', '丙': '火', '丁': '壬', '戊': '癸',
    '己': '甲', '庚': '乙', '辛': '丙', '壬': '丁', '癸': '戊'
}

def get_nayin_element(na_yin_str):
    """Extract element (木, 火, 土, 金, 水) from Na Yin string."""
    if not na_yin_str: return None
    for e in ['木', '火', '土', '金', '水']:
        if e in na_yin_str: return e
    return None

def is_element_countering(e1, e2):
    """Does e1 counter e2?"""
    rules = {
        '木': '土',
        '土': '水',
        '水': '火',
        '火': '金',
        '金': '木'
    }
    return rules.get(e1) == e2

def get_branch_relationship(b1, b2):
    """
    Check relationship between two branches.
    Returns: '冲', '刑', '破', '害', '六合', '暗合' or None.
    Prioritizes stronger interactions: 冲 > 刑 > 害 > 破 > 合.
    """
    if not b1 or not b2: return None
    
    # Sort for consistent pair lookup
    pair = tuple(sorted([b1, b2]))
    
    def normalize_pairs(pair_list):
        return set(tuple(sorted(p)) for p in pair_list)

    # 1. 冲 (Clash)
    chong_pairs = normalize_pairs([
        ('子', '午'), ('丑', '未'), ('寅', '申'),
        ('卯', '酉'), ('辰', '戌'), ('巳', '亥')
    ])
    if pair in chong_pairs: return '冲'
    
    # 2. 刑 (Punishment)
    # Zi-Mao
    if pair == tuple(sorted(('子', '卯'))): return '刑'
    # Self-Xing
    if b1 == b2 and b1 in ['辰', '午', '酉', '亥']: return '刑'
    # San Xing Partial
    xing_pairs = normalize_pairs([
        ('寅', '巳'), ('巳', '申'), ('寅', '申'),
        ('丑', '戌'), ('戌', '未'), ('丑', '未')
    ])
    if pair in xing_pairs: return '刑'
    
    # 3. 害 (Harm)
    hai_pairs = normalize_pairs([
        ('子', '未'), ('丑', '午'), ('寅', '巳'),
        ('卯', '辰'), ('申', '亥'), ('酉', '戌')
    ])
    # Note: Yin-Si is also Xing, handled above. 
    # If logic requires all, we might need a list. But prompt implies "Interaction exists".
    if pair in hai_pairs: return '害'
    
    # 4. 破 (Destruction)
    po_pairs = normalize_pairs([
        ('子', '酉'), ('丑', '辰'), ('寅', '亥'), # Yin-Hai is also He
        ('卯', '午'), ('巳', '申'), # Si-Shen is also He / Xing
        ('未', '戌')
    ])
    # Filter out ones that are He or Xing if we prioritize, but strict definition of Po:
    if pair in po_pairs: 
        # Yin-Hai is He (Wood), also Po? usually considered He.
        # Si-Shen is He (Water), also Xing/Po.
        return '破'
        
    # 5. 六合 (Six Harmony)
    he_pairs = normalize_pairs([
        ('子', '丑'), ('寅', '亥'), ('卯', '戌'),
        ('辰', '酉'), ('巳', '申'), ('午', '未')
    ])
    if pair in he_pairs: return '六合'
    
    # 6. 暗合 (Secret Harmony)
    an_he_pairs = normalize_pairs([
       ('寅', '丑'),
       ('午', '亥'),
       ('卯', '申'),
       ('子', '巳')
    ])
    if pair in an_he_pairs: return '暗合'
    
    return None

def check_eating_god_meets_owl(processed_pillars):
    return check_owl_devours_eating_god_logic(processed_pillars)

def analyze_risks(processed_pillars, info=None):
    """
    Master function to check Life/Death risks.
    Mainly checks Structural Risks (Eating God) for the specific time slice.
    Timeline events (SYBL, FYFY, TCO) are handled by get_future_risk_years.
    """
    all_results = []
    
    # Eating God Meets Owl (食神逢枭 / 枭神夺食)
    egmo = check_owl_devours_eating_god_logic(processed_pillars)
    if egmo: all_results.extend(egmo)
    
    # Yang Ren Feng Chong (羊刃逢冲)
    yrc = check_yang_ren_chong(processed_pillars)
    if yrc: all_results.extend(yrc)
    
    # Set default category 'RISK' for legacy/standard risks if missing
    for r in all_results:
        if 'category' not in r:
            r['category'] = 'RISK'
    
    # --- New Oral Secrets (秘诀) ---
    
    # Secret 1: 年比月比偏财隐，父亲早逝
    if len(processed_pillars) >= 2:
        p0_ten = processed_pillars[0].get('tenGod', '')
        p1_ten = processed_pillars[1].get('tenGod', '')
        if '比' in p0_ten and '比' in p1_ten:
            # Check for Indirect Wealth (偏财/才) on stems 0-3
            stems_ten = [p.get('tenGod', '') for p in processed_pillars[:4]]
            has_iw_on_stem = any('才' in t for t in stems_ten)
            if not has_iw_on_stem:
                all_results.append({
                    'title': "秘诀：比肩丛生父早逝",
                    'description': "年比月比偏财隐，父亲早逝。断语：年干及月干均为比肩，且偏财星不在天干。",
                    'probability': "高",
                    'trigger_type': 'ORIGINAL'
                })

    # Secret 2: 年支月支皆正财，母缘浅薄或早殇
    if len(processed_pillars) >= 2:
        y_hidden = processed_pillars[0].get('hidden', [])
        m_hidden = processed_pillars[1].get('hidden', [])
        y_main_god = y_hidden[0].get('god', '') if y_hidden else ''
        m_main_god = m_hidden[0].get('god', '') if m_hidden else ''
        if '财' in y_main_god and '财' in m_main_god:
             # '财' matches '正财' but not '才' (偏财) usually.
             all_results.append({
                'title': "秘诀：正财重重母缘薄",
                'description': "年支月支皆正财，母缘浅薄或早殇。断语：年支与月支的主气均为正财星。",
                'probability': "高",
                'trigger_type': 'ORIGINAL'
            })

    # Secret 3: 年伤月枭，父埋母病
    if len(processed_pillars) >= 2:
        p0_ten = processed_pillars[0].get('tenGod', '')
        p1_ten = processed_pillars[1].get('tenGod', '')
        is_owl = '枭' in p1_ten or '偏印' in p1_ten
        if '伤' in p0_ten and is_owl:
            all_results.append({
                'title': "秘诀：年伤月枭",
                'description': "年伤月枭，父埋母病。断语：年干见伤官，月干见枭神（偏印）。",
                'probability': "高",
                'trigger_type': 'ORIGINAL'
            })

    # Secret 5: 刑冲破印母他乡
    # Logic: 
    # 1. Identify "Seal" (Zheng Yin > Pian Yin). Check if damaged (Star Damage).
    # 2. ALSO check Month Branch (Palace Damage).
    # 3. If both, it's a "Typical Case" (典型案例).
    
    star_idx = -1
    star_source = ''

    def find_branch_with_god(kws):
        for i in range(min(4, len(processed_pillars))):
            hidden = processed_pillars[i].get('hidden', [])
            for h in hidden:
                god_str = h.get('god', '')
                if any(kw in god_str for kw in kws):
                    return i
        return -1

    # 1. Find Seal (Star)
    star_idx = find_branch_with_god(['正印', '印'])
    if star_idx != -1:
        star_source = '正印'
    else:
        star_idx = find_branch_with_god(['偏印', '枭'])
        if star_idx != -1:
            star_source = '偏印'
            
    is_star_damaged = False
    is_palace_damaged = False
    star_damage_info = ''
    palace_damage_info = ''
    
    # Check Star Damage
    if star_idx != -1 and star_idx < len(processed_pillars):
        target_zhi = processed_pillars[star_idx]['zhi']
        for i in range(min(4, len(processed_pillars))):
            if i == star_idx: continue
            other_zhi = processed_pillars[i]['zhi']
            rel = get_branch_relationship(target_zhi, other_zhi)
            if rel in ['冲', '刑', '破']:
                is_star_damaged = True
                star_damage_info = f"星({star_source}{target_zhi})受{rel}"
                break
                
    # Check Palace Damage (Month Branch - Index 1)
    if len(processed_pillars) > 1:
        m_zhi = processed_pillars[1].get('zhi')
        if m_zhi:
            for i in range(min(4, len(processed_pillars))):
                if i == 1: continue
                other_zhi = processed_pillars[i]['zhi']
                rel = get_branch_relationship(m_zhi, other_zhi)
                if rel in ['冲', '刑', '破']:
                    is_palace_damaged = True
                    palace_damage_info = f"宫(月支{m_zhi})受{rel}"
                    break
                    
    if is_star_damaged or is_palace_damaged:
        desc = "刑冲破印母他乡。断语："
        if is_star_damaged and is_palace_damaged:
            desc += f"典型案例！{star_damage_info}且{palace_damage_info}，印星与月令母宫同时受损，主母亲缘分极薄、多病或离散。"
        elif is_star_damaged:
            desc += f"{star_damage_info}，主母亲缘分薄、远走他乡或工作不稳定。"
        else:
            desc += f"{palace_damage_info}，虽印星未损，但母宫受损，亦主母亲缘分薄或不安稳。"
            
        all_results.append({
            'title': "秘诀：刑冲破印母他乡",
            'description': desc,
            'probability': "高",
            'trigger_type': 'ORIGINAL'
        })
        
    # Secret 6: 二重亡神母先丧
    wang_shen_count = 0
    for p in processed_pillars[:4]:
        ss = p.get('shenSha', [])
        if '亡神' in ss:
            wang_shen_count += 1
            
    if wang_shen_count >= 2:
        all_results.append({
            'title': "秘诀：二重亡神母先丧",
            'description': "二重亡神母先丧。断语：命局中出现两个或以上亡神，主母亲身体不佳或先于父亲去世。",
            'probability': "高",
            'trigger_type': 'ORIGINAL'
        })
        
    # Secret 7: 时杀带花父先亡
    if len(processed_pillars) >= 4:
        h_pillar = processed_pillars[3]
        h_ten_god = h_pillar.get('tenGod', '')
        h_shen_sha = h_pillar.get('shenSha', [])
        
        # Check Seven Killings
        is_qi_sha = '杀' in h_ten_god or '七杀' in h_ten_god or '偏官' in h_ten_god
        
        # Check Flower
        has_flower = '咸池' in h_shen_sha or '桃花' in h_shen_sha
        
        if is_qi_sha and has_flower:
            all_results.append({
                'title': "秘诀：时杀带花父先亡",
                'description': "时杀带花父先亡。断语：时干为七杀，且时支临咸池或桃花，主父亲恐先于母亲去世。",
                'probability': "高",
                'trigger_type': 'ORIGINAL'
            })
    
    # Secret 8: 日支羊刃他处见，配偶早丧 (Static)
    # Check Day Yang Ren first
    if len(processed_pillars) >= 3:
        dm_gan = processed_pillars[2]['gan']
        day_zhi = processed_pillars[2]['zhi']
        YANG_REN_MAP = {
            '甲': '卯', '乙': '寅', '丙': '午', '丁': '巳', '戊': '午',
            '己': '巳', '庚': '酉', '辛': '申', '壬': '子', '癸': '亥'
        }
        sheep_blade_zhi = YANG_REN_MAP.get(dm_gan)
        
        # Only proceed if Day Branch IS Yang Ren
        if sheep_blade_zhi and day_zhi == sheep_blade_zhi:
            # Condition 1: Check if Yang Ren appears elsewhere (Year, Month, Hour)
            other_yang_ren_count = 0
            check_indices = [0, 1, 3]
            for idx in check_indices:
                if idx < len(processed_pillars) and processed_pillars[idx]['zhi'] == sheep_blade_zhi:
                    other_yang_ren_count += 1
            
            if other_yang_ren_count > 0:
                all_results.append({
                    'title': "秘诀：日支羊刃他处见",
                    'description': f"日支羊刃他处见，配偶早丧。断语：日支为羊刃({day_zhi})，且在年/月/时支再次出现({other_yang_ren_count}个)。",
                    'probability': "高",
                    'trigger_type': 'ORIGINAL'
                })

    # Secret 10: 日支被月时双冲，婚破偶病
    if len(processed_pillars) >= 4:
        d_zhi = processed_pillars[2]['zhi']
        m_zhi = processed_pillars[1]['zhi']
        h_zhi = processed_pillars[3]['zhi']
        
        m_rel = get_branch_relationship(d_zhi, m_zhi)
        h_rel = get_branch_relationship(d_zhi, h_zhi)
        
        if m_rel == '冲' and h_rel == '冲':
            all_results.append({
                'title': "秘诀：日支被月时双冲",
                'description': f"日支被月时双冲，婚破偶病。断语：日支({d_zhi})同时被月支({m_zhi})与时支({h_zhi})相冲，主婚姻破裂或配偶多病灾。",
                'probability': "高",
                'trigger_type': 'ORIGINAL'
            })
    


    # Secret 11: 二官/财争合日
    # Logic: Identify Stem that combines with Day Master (GAN_HE_MAP matches).
    # If Count >= 2 in Year/Month/Hour:
    day_gan = processed_pillars[2]['gan'] if len(processed_pillars) > 2 else None
    combine_gan = GAN_HE.get(day_gan)
    if combine_gan:
        combine_count = 0
        for idx in [0, 1, 3]:
            if idx < len(processed_pillars) and processed_pillars[idx]['gan'] == combine_gan:
                combine_count += 1
        
        if combine_count >= 2:
            gender = info.get('gender') if info else None
            is_male = (gender == 1 or gender == '1' or gender == '男')
            is_yang_dm = day_gan in ["甲", "丙", "戊", "庚", "壬"]
            
            # Male + Yang DM (Combine with Cai)
            if is_male and is_yang_dm:
                all_results.append({
                    'title': "秘诀：二财争合 (男命)",
                    'description': f"男命天干二财争合日主，三妻四妾。断语：日主({day_gan})与天干({combine_gan})(正财)相合，且({combine_gan})出现{combine_count}次，主感情复杂，多妻多恋。",
                    'probability': "高",
                    'trigger_type': 'ORIGINAL'
                })
            # Female + Yin DM (Combine with Guan)
            elif (not is_male) and (not is_yang_dm):
                all_results.append({
                    'title': "秘诀：二官争合 (女命)",
                    'description': f"女命天干二官争合日主，多婚之象。断语：日主({day_gan})与天干({combine_gan})(正官)相合，且({combine_gan})出现{combine_count}次，主婚姻多变，易多婚或出轨。",
                    'probability': "高",
                    'trigger_type': 'ORIGINAL'
                })


    # Secret 12: 日坐华盖合驿马
    d_zhi = processed_pillars[2]['zhi']
    d_shen_sha = processed_pillars[2].get('shen_sha', [])
    if '华盖' in d_shen_sha:
        yi_ma_set = {'寅', '申', '巳', '亥'}
        for idx in [0, 1, 3]:
            if idx < len(processed_pillars):
                target_zhi = processed_pillars[idx]['zhi']
                if target_zhi in yi_ma_set:
                    rel = get_branch_relationship(d_zhi, target_zhi)
                    key = "".join(sorted([d_zhi, target_zhi]))
                    is_extra_combo = key in ['寅戌', '巳丑', '申辰', '亥未', '寅辰', '亥丑', '巳未', '申戌']
                    if rel == '六合' or is_extra_combo:
                        all_results.append({
                            'title': "秘诀：日坐华盖合驿马",
                            'description': f"日坐华盖合驿马，同床异梦。断语：日支({d_zhi})为华盖，且与原局驿马支({target_zhi})相合，主夫妻间缺乏沟通，价值观不一。",
                            'probability': "中",
                            'trigger_type': 'ORIGINAL'
                        })


    # Secret 13: 日时对冲，分道扬镳
    if len(processed_pillars) >= 4:
        h_zhi = processed_pillars[3]['zhi']
        if get_branch_relationship(d_zhi, h_zhi) == '冲':
            all_results.append({
                'title': "秘诀：日时对冲",
                'description': f"日时对冲，分道扬镳。断语：日支({d_zhi})与时支({h_zhi})相冲，主夫妻间易产生剧烈矛盾，甚至离婚之象。",
                'probability': "中",
                'trigger_type': 'ORIGINAL'
            })


    # Secret 14: 女命时支正印多，克子
    gender = info.get('gender') if info else None
    is_female = (gender == 0 or gender == '0' or gender == '女')
    if is_female and len(processed_pillars) >= 4:
        h_hidden = processed_pillars[3].get('hidden', [])
        h_has_zheng_yin = any(h.get('name') == '正印' for h in h_hidden)
        
        if h_has_zheng_yin:
            other_zheng_yin_count = 0
            for idx in [0, 1, 2]:
                hidden = processed_pillars[idx].get('hidden', [])
                if any(h.get('name') == '正印' for h in hidden):
                    other_zheng_yin_count += 1
            
            if other_zheng_yin_count >= 1:
                all_results.append({
                    'title': "秘诀：女命时支正印多",
                    'description': f"女命时支正印多，克子之象。断语：命主为女性，时支含有正印，且年/月/日支中亦有正印出现，主子缘较薄，或仅有女儿。",
                    'probability': "中",
                    'trigger_type': 'ORIGINAL'
                })


    # Secret 15: 时柱空亡，儿女缘浅
    if len(processed_pillars) >= 4:
        d_pillar = processed_pillars[2]
        h_zhi = processed_pillars[3]['zhi']
        d_kong_wang = d_pillar.get('kong_wang', [])
        
        # d_kong_wang is usually a list like ['戌', '亥']
        if h_zhi in d_kong_wang:
            all_results.append({
                'title': "秘诀：时柱空亡",
                'description': f"时柱空亡，儿女缘浅。断语：时支({h_zhi})处于日柱({d_pillar['gan']}{d_pillar['zhi']})的空亡位({''.join(d_kong_wang)})，主子孙缘分较薄，或容易有流产、损子之忧。",
                'probability': "中",
                'trigger_type': 'ORIGINAL'
            })


    # Secret 16: 年月刑冲父子离
    if len(processed_pillars) >= 2:
        y_zhi = processed_pillars[0]['zhi']
        m_zhi = processed_pillars[1]['zhi']
        rel = get_branch_relationship(y_zhi, m_zhi)
        if rel in ['刑', '冲']:
            all_results.append({
                'title': "秘诀：年月刑冲父子离",
                'description': f"年月刑冲父子离。断语：年支({y_zhi})与月支({m_zhi})相{rel}，主父亲常年在外工作，或命主与双亲缘分较薄，早年离家。",
                'probability': "中",
                'trigger_type': 'ORIGINAL'
            })


    # Secret 17: 戊甲重克头面疤
    if len(processed_pillars) >= 4:
        count_jia = 0
        count_wu = 0
        for idx in [0, 1, 3]:
            gan = processed_pillars[idx].get('gan')
            if gan == '甲':
                count_jia += 1
            elif gan == '戊':
                count_wu += 1
        
        if (count_jia == 2 and count_wu == 1) or (count_jia == 1 and count_wu == 2):
            all_results.append({
                'title': "秘诀：戊甲重克头面疤",
                'description': "戊甲重克头面疤。天干见两甲克一戊或一甲克两戊（不含日柱），主头面部易受伤留疤，或有明显胎记、瑕疵。",
                'probability': "中",
                'trigger_type': 'ORIGINAL'
            })


    # Secret 18 & 19: 酉亥与辰戌酉亥
    if len(processed_pillars) >= 4:
        original_zhis = [p.get('zhi') for p in processed_pillars[:4]]
        has_you = '酉' in original_zhis
        has_hai = '亥' in original_zhis
        has_chen = '辰' in original_zhis
        has_xu = '戌' in original_zhis
        
        if has_chen and has_xu and has_you and has_hai:
            all_results.append({
                'title': "秘诀：地支辰戌酉亥全齐",
                'description': "地支辰戌酉亥全齐。断语：地支集齐辰戌酉亥，性格极端火爆，易因冲动招惹官非，并需防范突发性短命之灾。",
                'probability': "高",
                'trigger_type': 'ORIGINAL'
            })
        elif has_you and has_hai:
            all_results.append({
                'title': "秘诀：地支酉亥",
                'description': "地支见酉和亥。断语：地支见酉和亥，主性格风流、纵欲，需防酒色过度伤害身体，影响寿元。",
                'probability': "中",
                'trigger_type': 'ORIGINAL'
            })


    # Secret 20: 地支一卯二卯，富贵到老
    if len(processed_pillars) >= 4:
        mao_count = sum(1 for p in processed_pillars[:4] if p.get('zhi') == '卯')
        if mao_count in [1, 2]:
            all_results.append({
                'title': "秘诀：地支一二卯",
                'description': "地支见一二卯。断语：命局地支见一或两个卯木，主富贵到老，衣食无忧，晚年富贵。",
                'probability': "中",
                'trigger_type': 'ORIGINAL',
                'category': 'GOOD'
            })

    # Secret 21: 禄多则贫
    if len(processed_pillars) >= 4:
        lu_map = {
            '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午', 
            '戊': '巳', '己': '午', '庚': '申', '辛': '酉', 
            '壬': '亥', '癸': '子'
        }
        dm_gan = processed_pillars[2].get('gan')
        lu_zhi = lu_map.get(dm_gan)
        if lu_zhi:
            lu_count = sum(1 for p in processed_pillars[:4] if p.get('zhi') == lu_zhi)
            if lu_count >= 3:
                all_results.append({
                    'title': "秘诀：禄多则贫",
                    'description': f"命局禄神过多。断语：禄神({lu_zhi})多达三个及以上，主奔波劳心，求财辛苦，反主贫穷。",
                    'probability': "中",
                    'trigger_type': 'ORIGINAL'
                })

    # Secret 22: 驿马星多，身体多病
    if len(processed_pillars) >= 4:
        yima_branches = ['寅', '申', '巳', '亥']
        yima_count = sum(1 for p in processed_pillars[:4] if p.get('zhi') in yima_branches)
        if yima_count >= 3:
            all_results.append({
                'title': "秘诀：驿马星多",
                'description': "命局驿马星过多。断语：地支见三个及以上驿马星(寅申巳亥)，主身体素质较差，容易生病。",
                'probability': "中",
                'trigger_type': 'ORIGINAL'
            })


    # Secret 23: 两头挂
    if len(processed_pillars) >= 4:
        def get_category(god):
            if god in ['正印', '偏印']: return '印星'
            if god == '伤官': return '伤官'
            if god == '食神': return '食神'
            if god == '七杀': return '七杀'
            if god in ['正财', '偏财']: return '财星'
            if god in ['比肩', '劫财']: return '比劫'
            if god == '正官': return '正官'
            return None

        y_stem_cat = get_category(processed_pillars[0].get('tenGod'))
        h_stem_cat = get_category(processed_pillars[3].get('tenGod'))
        
        y_branch_god = processed_pillars[0].get('hidden', [{}])[0].get('god', '')
        h_branch_god = processed_pillars[3].get('hidden', [{}])[0].get('god', '')
        y_branch_cat = get_category(y_branch_god)
        h_branch_cat = get_category(h_branch_god)

        match_cat = None
        if y_stem_cat and y_stem_cat == h_stem_cat:
            match_cat = y_stem_cat
        elif y_branch_cat and y_branch_cat == h_branch_cat:
            match_cat = y_branch_cat

        if match_cat:
            descs = {
                '印星': '心地善良，有爱心，易亲近宗教/玄学/艺术。风险提示：容易过于清高或孤僻。',
                '伤官': '六亲缘薄，与家人疏远；口才好但易伤人，爱抬杠；才华横溢但恃才傲物。风险提示：宜远走他乡发展，少言慎行。追加：腿部易受伤留疤，需防范长短腿或断腿风险。',
                '食神': '一生口福好，能吃百家饭（人缘好），技艺精湛；心态乐观，不愁吃喝。风险提示：注意发胖或过于安逸。',
                '七杀': '一生多灾多难，易招官非诉讼，事业起伏大；男命则子嗣缘分较迟或较薄。风险提示：风险极大，宜修身养性，利用七杀能量做武职或管理。追加：腿部易受伤留疤，需防范长短腿或断腿风险。',
                '财星': '出手大方，存不住钱（财露白）；多半会远离家乡发展。风险提示：宜置办固定资产强制储蓄。',
                '比劫': '易因朋友/合伙破财，招小人；性格固执，自尊心强；兄弟姐妹缘薄或竞争激烈。风险提示：避免合伙，财务独立。',
                '正官': '事业稳定，福禄长久，社会地位高；为人正派，循规蹈矩。风险提示：相对最稳的格局，但可能缺乏爆发力。'
            }
            all_results.append({
                'title': f"秘诀：{match_cat}两头挂",
                'description': f"{match_cat}两头挂。断语：{descs[match_cat]}",
                'probability': "中",
                'trigger_type': 'ORIGINAL'
            })

    # Secret 24: 月支断痣
    if len(processed_pillars) >= 4:
        m_zhi = processed_pillars[1].get('zhi')
        mole_map = {
            '子': '胸部正中 / 锁骨下区域',
            '丑': '腹部下方 (肚脐下)',
            '寅': '私密处 / 腹股沟 / 发际线',
            '卯': '胸部两侧 / 乳房附近',
            '辰': '腹部上方 (肚脐上)',
            '巳': '私密器官 / 腹股沟 (易烫伤疤)',
            '午': '胸口正中 (膻中穴)',
            '未': '腹部下方 / 小腹',
            '申': '腹股沟 / 背部边缘',
            '酉': '胸部两侧 / 肋骨',
            '戌': '腹部上方 / 胃部',
            '亥': '私密器官 / 大腿根部'
        }
        
        mole_loc = mole_map.get(m_zhi)
        if mole_loc:
            all_results.append({
                'title': "秘诀：月支断痣",
                'description': f"月支为{m_zhi}。推断位置：{mole_loc}。",
                'probability': "中",
                'trigger_type': 'ORIGINAL',
                'category': 'INFO'
            })
    
    # Secret 25: 卧室风水 (床下物件) - Merged
    if len(processed_pillars) >= 4:
        branch_obj_map = {
            '子': '积水或杂乱电子线', '丑': '整齐收纳的旧物',
            '寅': '枯萎绿植或旧书', '卯': '干净折叠的衣物',
            '辰': '破损容器或积水', '巳': '常用电子设备',
            '午': '闲置电器或易燃物', '未': '存放整齐的食品',
            '申': '尖锐金属物品', '酉': '贵重首饰收纳盒',
            '戌': '杂乱无章的杂物', '亥': '常用电子设备'
        }

        god_obj_map = {
            '正官': '重要工作资料', '七杀': '合照、相框、照片、挂画、手办、悬挂小物品；玩偶摆件或带尖角的摆件(供奉)',
            '正财': '贵重物品收纳盒', '偏财': '杂物堆积，杂乱无章',
            '正印': '书籍或相册', '偏印': '跟翅膀和羽毛相关的物品',
            '食神': '零食或健身器材', '伤官': '艺术创作工具',
            '比肩': '他人遗留物品', '劫财': '实用工具'
        }

        check_pillars = [
            {'idx': 2, 'name': '日支'},
            {'idx': 3, 'name': '时支'}
        ]

        combined_desc = []

        for item in check_pillars:
            p = processed_pillars[item['idx']]
            zhi = p.get('zhi')
            
            # Get Main Qi (First item in 'hidden' list)
            main_qi_god = ''
            hidden_list = p.get('hidden', [])
            if hidden_list and len(hidden_list) > 0:
                main_qi_god = hidden_list[0].get('god', '')
            
            parts = []
            # 1. Branch Map
            if zhi in branch_obj_map:
                parts.append(f"【{zhi}】可能对应：{branch_obj_map[zhi]}")
            
            # 2. Ten God Map (Main Qi)
            if main_qi_god and main_qi_god in god_obj_map:
                parts.append(f"【{main_qi_god}】可能对应：{god_obj_map[main_qi_god]}")
            
            if parts:
                desc_str = "；".join(parts)
                combined_desc.append(f"{item['name']}：{zhi}({main_qi_god or '无藏干'})。{desc_str}。")

        if combined_desc:
            all_results.append({
                'title': "秘诀：卧室风水",
                'description': "<br/>".join(combined_desc),
                'probability': "中",
                'trigger_type': 'ORIGINAL',
                'category': 'INFO'
            })

    # Apply Categories and Defaults
    for r in all_results:
        t = r.get('title', '')
        if '断痣' in t:
            r['category'] = 'INFO'
        elif '一二卯' in t:
            r['category'] = 'GOOD'
        elif 'category' not in r:
            r['category'] = 'RISK'

    # Deduplicate
    unique_results = []
    seen = set()
    for res in all_results:
        key = (res['title'], res['description'])
        if key not in seen:
            seen.add(key)
            unique_results.append(res)
            
    # Sort
    cat_order = {'RISK': 1, 'GOOD': 2, 'INFO': 3}
    unique_results.sort(key=lambda x: cat_order.get(x.get('category', 'RISK'), 99))
            
    
    # Sort
    cat_order = {'RISK': 1, 'GOOD': 2, 'INFO': 3}
    unique_results.sort(key=lambda x: cat_order.get(x.get('category', 'RISK'), 99))
            
    return unique_results

def get_future_risk_years(data):
    """
    Scan all Da Yun and Liu Nian to find future risk years (SYBL, Fan Yin, Fu Yin, TCO).
    """
    forecast = []
    
    # Base Pillars (Year, Month, Day, Hour)
    base_pillars = data.get('pillars', [])
    if len(base_pillars) != 4: return []
    
    # Helper to format luck
    def format_luck(l_obj):
        gz = l_obj.get('ganZhi', '')
        g = gz[0] if len(gz)>0 else ''
        z = gz[1] if len(gz)>1 else ''
        return {
            'gan': g, 'zhi': z,
            'tenGod': l_obj.get('tenGod', ''),
            'hidden': l_obj.get('hidden', []),
            'ganZhi': gz,
            'naYin': l_obj.get('naYin', '')
        }
    
    da_yun_list = data.get('daYunList', [])
    
    for dy in da_yun_list:
        dy_pillar = format_luck(dy)
        
        for ln in dy.get('liuNian', []):
            ln_pillar = format_luck(ln)
            
            # Construct 6 pillars
            test_pillars = base_pillars + [dy_pillar, ln_pillar]
            
            # Check SYBL
            sybl = check_sui_yun_bing_lin(test_pillars)
            for r in sybl:
                forecast.append({
                    'year': ln['year'],
                    'ganZhi': ln['ganZhi'],
                    'risk': r['title'],
                    'desc': r['description'],
                    'trigger_type': 'LN'
                })
                
            # Check FYFY
            fyfy = check_fan_yin_fu_yin(test_pillars)
            for r in fyfy:
                forecast.append({
                    'year': ln['year'],
                    'ganZhi': ln['ganZhi'],
                    'risk': r['title'],
                    'desc': r['description'],
                    'trigger_type': 'LN'
                })
                
            # Check TCO
            tco = check_three_clash_one(test_pillars)
            for r in tco:
                forecast.append({
                    'year': ln['year'],
                    'ganZhi': ln['ganZhi'],
                    'risk': r['title'],
                    'desc': r['description'],
                    'trigger_type': 'LN'
                })
            
            # Check Eating God Meets Owl (Dynamic / Luck Triggered Only)
            egmo = check_owl_devours_eating_god_logic(test_pillars)
            for r in egmo:
                t_type = r.get('trigger_type', 'BOTH')
                # Rewrite title if needed to match "枭神夺食" standard
                title = r['title'].replace("食神逢枭", "枭神夺食")
                
                if t_type != 'ORIGINAL':
                    forecast.append({
                        'year': ln['year'],
                        'ganZhi': ln['ganZhi'],
                        'risk': title,
                        'desc': r['description'],
                        'trigger_type': t_type,
                        'dy_name': f"{dy_pillar['gan']}{dy_pillar['zhi']}"
                    })
            
            # Check Yang Ren Feng Chong (Dynamic / Luck Triggered Only)
            yrc = check_yang_ren_chong(test_pillars)
            for r in yrc:
                t_type = r.get('trigger_type', 'BOTH')
                if t_type != 'ORIGINAL':
                    forecast.append({
                        'year': ln['year'],
                        'ganZhi': ln['ganZhi'],
                        'risk': r['title'],
                        'desc': r['description'],
                        'trigger_type': t_type,
                        'dy_name': f"{dy_pillar['gan']}{dy_pillar['zhi']}"
                    })
                
            # Secret 4: 年纳音被月克，岁运再克父必亡
            y_ny_str = base_pillars[0].get('naYin', '')
            m_ny_str = base_pillars[1].get('naYin', '')
            y_ny = get_nayin_element(y_ny_str)
            m_ny = get_nayin_element(m_ny_str)
            
            if y_ny and m_ny and is_element_countering(m_ny, y_ny):
                # Static part met, check Sui/Yun
                dy_ny = get_nayin_element(dy_pillar.get('naYin', ''))
                ln_ny = get_nayin_element(ln_pillar.get('naYin', ''))
                
                if is_element_countering(dy_ny, y_ny) or is_element_countering(ln_ny, y_ny):
                    forecast.append({
                        'year': ln['year'],
                        'ganZhi': ln['ganZhi'],
                        'risk': "秘诀：纳音克父",
                        'desc': f"年纳音被月克，岁运再克父必亡。原因：年柱纳音({y_ny_str})被月柱纳音({m_ny_str})所克，当前大运/流年纳音再次克年柱。",
                        'trigger_type': 'LN',
                        'dy_name': f"{dy_pillar['gan']}{dy_pillar['zhi']}"
                    })
            
            # Secret 9: 日坐羊刃逢冲，配偶血光早亡 (Dynamic)
            # Needs base pillars to determine Day Branch and Day Master
            if len(base_pillars) >= 3:
                dm_gan_b = base_pillars[2]['gan']
                day_zhi_b = base_pillars[2]['zhi']
                YANG_REN_MAP_B = {
                    '甲': '卯', '乙': '寅', '丙': '午', '丁': '巳', '戊': '午',
                    '己': '巳', '庚': '酉', '辛': '申', '壬': '子', '癸': '亥'
                }
                sheep_blade_zhi_b = YANG_REN_MAP_B.get(dm_gan_b)
                
                if sheep_blade_zhi_b and day_zhi_b == sheep_blade_zhi_b:
                    # Check if DY or LN clashes DAY BRANCH specifically
                    has_chong = False
                    chong_source = []
                    
                    # Check DY
                    dy_rel = get_branch_relationship(day_zhi_b, dy_pillar['zhi'])
                    if dy_rel == '冲':
                        has_chong = True
                        chong_source.append(f"大运({dy_pillar['zhi']})")
                        
                    # Check LN
                    ln_rel = get_branch_relationship(day_zhi_b, ln_pillar['zhi'])
                    if ln_rel == '冲':
                        has_chong = True
                        chong_source.append(f"流年({ln_pillar['zhi']})")
                        
                    if has_chong:
                        source_str = "与".join(chong_source)
                        forecast.append({
                            'year': ln['year'],
                            'ganZhi': ln['ganZhi'],
                            'risk': "秘诀：配偶血光",
                            'desc': f"日坐羊刃逢冲，配偶血光早亡。原因：日支羊刃({day_zhi_b})逢{source_str}相冲。",
                            'trigger_type': 'LN',
                            'dy_name': f"{dy_pillar['gan']}{dy_pillar['zhi']}"
                        })

                
                # Secret 12: 日坐华盖合驿马 (Dynamic)
                d_shen_sha_dyn = base_pillars[2].get('shen_sha', [])
                if '华盖' in d_shen_sha_dyn:
                    yi_ma_set_dyn = {'寅', '申', '巳', '亥'}
                    check_branches = [dy_pillar['zhi'], ln_pillar['zhi']]
                    for target_zhi_dyn in check_branches:
                        if target_zhi_dyn in yi_ma_set_dyn:
                            rel_dyn = get_branch_relationship(day_zhi_b, target_zhi_dyn)
                            key_dyn = "".join(sorted([day_zhi_b, target_zhi_dyn]))
                            is_extra_combo_dyn = key_dyn in ['寅戌', '巳丑', '申辰', '亥未', '寅辰', '亥丑', '巳未', '申戌']
                            if rel_dyn == '六合' or is_extra_combo_dyn:
                                forecast.append({
                                    'year': ln['year'],
                                    'ganZhi': ln['ganZhi'],
                                    'risk': "秘诀：华盖合驿马 (同床异梦)",
                                    'desc': f"该年/运支({target_zhi_dyn})为驿马并与日支华盖({day_zhi_b})相合，代表在该年/大运期间夫妻可能沟通不畅、价值观有分歧。",
                                    'trigger_type': 'LN',
                                    'dy_name': f"{dy_pillar['gan']}{dy_pillar['zhi']}"
                                })

    # Sort by year
    forecast.sort(key=lambda x: x['year'])
    return forecast

def check_fan_yin_fu_yin(processed_pillars):
    """
    Check for Fan Yin (Reverse Chant) and Fu Yin (Hidden Chant) affecting Day Pillar.
    Target: Day Pillar (Index 2).
    Source: Da Yun (4) and Liu Nian (5).
    Condition: MUST BE SIMULTANEOUS interactions from BOTH Da Yun and Liu Nian.
    """
    if len(processed_pillars) < 6: return []
    
    # Define local WX mapping to avoid scope issues
    LOCAL_WX = {
        '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
        '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
        '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土',
        '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金',
        '戌': '土', '亥': '水'
    }

    day = processed_pillars[2]
    dy = processed_pillars[4]
    ln = processed_pillars[5]
    
    # Helpers
    stem_order = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    def is_tian_ke(s1, s2):
        if not s1 or not s2: return False
        try:
            i1 = stem_order.index(s1)
            i2 = stem_order.index(s2)
            diff = abs(i1 - i2)
            return diff == 6 or diff == 4 
        except: return False

    def is_di_chong(b1, b2):
        pair = tuple(sorted([b1, b2]))
        chong_pairs = [
            ('子', '午'), ('丑', '未'), ('寅', '申'),
            ('卯', '酉'), ('辰', '戌'), ('巳', '亥')
        ]
        return pair in [tuple(sorted(p)) for p in chong_pairs]
    
    def get_interaction_type(source_p):
        # Check Fu Yin
        if source_p['gan'] == day['gan'] and source_p['zhi'] == day['zhi']:
            return "伏吟"
        # Check Fan Yin
        if is_tian_ke(source_p['gan'], day['gan']) and is_di_chong(source_p['zhi'], day['zhi']):
            return "反吟"
        return None
        
    dy_type = get_interaction_type(dy)
    ln_type = get_interaction_type(ln)
    
    results = []
    
    # Requirement: BOTH must have an interaction type
    if dy_type and ln_type:
        title = f"{dy_type} / {ln_type} (岁运同时引动)"
        # Construct detailed description
        desc_parts = []
        desc_parts.append(f"大运{dy_type}日柱({dy['gan']}{dy['zhi']} vs {day['gan']}{day['zhi']})")
        desc_parts.append(f"流年{ln_type}日柱({ln['gan']}{ln['zhi']} vs {day['gan']}{day['zhi']})")
        
        full_desc = "，".join(desc_parts) + "。断语：反吟伏吟，不死也脱层皮。"
        
        results.append({
            "title": title,
            "description": full_desc,
            "probability": "极高"
        })
        
    return results
    


def check_three_clash_one(processed_pillars):
    """
    Check for Three Clashes One (三冲一).
    Condition: 3 identical branches (in Year/Month/Day/Hour/Yun/Nian) clash with 1 branch in Original Chart.
    """
    if len(processed_pillars) < 6: return []
    
    # Clash Map (Bi-directional)
    clash_map = {
        '子': '午', '午': '子',
        '丑': '未', '未': '丑',
        '寅': '申', '申': '寅',
        '卯': '酉', '酉': '卯',
        '辰': '戌', '戌': '辰',
        '巳': '亥', '亥': '巳'
    }
    
    dy = processed_pillars[4]
    ln = processed_pillars[5]
    
    # STRICT RULE: Da Yun and Liu Nian MUST have identical branches.
    # "Da Yun and Liu Nian have two identical branches... then Original has..."
    if dy['zhi'] != ln['zhi']:
        return []
        
    source_branch = dy['zhi']
    
    # Check if Original Chart (Indices 0-3) contains this branch
    original_branches = [p['zhi'] for p in processed_pillars[:4]]
    
    if source_branch not in original_branches:
        return []
        
    # At this point:
    # DY has 1, LN has 1 (Identical) -> 2 External
    # Original has at least 1 -> Total >= 3
    # Condition met.
    
    # Now check if they clash with a specific target in the Original Chart
    target = clash_map.get(source_branch)
    if not target: return []
    
    if target in original_branches:
        # Calculate strict counts for description
        org_count = original_branches.count(source_branch)
        total_count = org_count + 2
        
        results = [{
            "title": "三冲一 (必有生死灾)",
            "description": f"岁运地支相同({source_branch})与原局{org_count}个{source_branch}共聚，三冲一(冲原局{target})。断语：三冲一，必有生死灾。",
            "probability": "极高"
        }]
        return results
        
    return []

def check_sui_yun_bing_lin(processed_pillars):
    """
    Check for Sui Yun Bing Lin (Year and Luck Cycle are identical).
    indices: 4 is Da Yun, 5 is Liu Nian.
    """
    if len(processed_pillars) < 6: return []
    
    dy = processed_pillars[4]
    ln = processed_pillars[5]
    
    # Check strict identity of Gan and Zhi
    if dy['gan'] == ln['gan'] and dy['zhi'] == ln['zhi']:
        return [{
            "title": "岁运并临",
            "description": f"流年与大运干支相同({dy['gan']}{dy['zhi']})。断语：不死自己死亲人。",
            "probability": "极高"
        }]
    return []

def check_yang_ren_chong(processed_pillars):
    """
    Check for:
    1. Yang Ren Feng Chong (羊刃逢冲)
    2. Yang Ren Die Die (羊刃叠叠逢刑冲)
    Prerequisite: Yang Ren exists in Original Chart (Indices 0-3).
    Trigger: Clash (Chong) or Punishment (Xing) MUST come from Da Yun (4) or Liu Nian (5).
    """
    if len(processed_pillars) < 6: return []
    
    dm_gan = processed_pillars[2]['gan']
    YANG_REN_MAP = {
        '甲': '卯', '乙': '寅', '丙': '午', '丁': '巳', '戊': '午',
        '己': '巳', '庚': '酉', '辛': '申', '壬': '子', '癸': '亥'
    }
    yr_zhi = YANG_REN_MAP.get(dm_gan)
    if not yr_zhi: return []
    
    # 1. Count Yang Rens in Original Chart
    org_branches = [p['zhi'] for p in processed_pillars[:4]]
    yr_count_org = org_branches.count(yr_zhi)
    
    if yr_count_org == 0:
        return []
        
    # 2. Identify External Trigger (Chong or Xing)
    # The external branch (4,5) must participate in a '冲' or '刑' 
    # where at least one side is a Yang Ren (Original or External).
    external_indices = [4, 5]
    original_indices = [0, 1, 2, 3]
    
    triggers = []
    has_dy_trigger = False
    has_ln_trigger = False
    for ext_idx in external_indices:
        b_ext = processed_pillars[ext_idx]['zhi']
        for org_idx in original_indices:
            b_org = processed_pillars[org_idx]['zhi']
            # Only trigger if the ORIGINAL branch being hit is the Yang Ren
            if b_org == yr_zhi:
                rel = get_branch_relationship(b_ext, b_org)
                if rel in ['冲', '刑']:
                    triggers.append({'rel': rel, 'zhi_ext': b_ext, 'zhi_org': b_org, 'idx': ext_idx})
                    if ext_idx == 4: has_dy_trigger = True
                    if ext_idx == 5: has_ln_trigger = True
    
    if not triggers:
        return []
        
    has_dy_trigger = False
    has_ln_trigger = False
    
    # Re-scan to set flags correctly for metadata (removed strictly from triggers loop for clarity if needed, 
    # but actual logic was in triggers loop. Let's keep the flags set in loop or just check results)
    # Actually flags were set in loop in previous turn. 
    # Let's ensure flags are set
    for t in triggers:
        if t.get('idx') == 4: has_dy_trigger = True
        if t.get('idx') == 5: has_ln_trigger = True

    # 3. Decision Logic
    results = []
    # Revert to generic source for Title Grouping
    source = "(岁运引动)"
    
    # A. Case: Yang Ren Feng Chong (Single or Multiple)
    # Triggered by '冲'
    # LOGIC UPDATE: If we have multiple Yang Rens (Die Die), that condition allows for Chong OR Xing and is more severe.
    # The user requested to suppress the standard "Feng Chong" alert if "Die Die" is present to avoid duplicates.
    
    found_die_die = False
    
    # B. Case: Yang Ren Die Die (Multiple Yang Rens) - Checked FIRST or handled logically
    if yr_count_org >= 2:
        # Any trigger (Chong or Xing) involving the Yang Ren or hitting from the Yang Ren
        t = triggers[0]
        trigger_rel = t['rel']
        trigger_desc = f"{t['zhi_ext']}与{t['zhi_org']}发生{trigger_rel}"
        
        results.append({
            "title": f"羊刃叠叠逢刑冲 {source}",
            "description": f"原局羊刃({yr_zhi})叠见({yr_count_org}个)且岁运引发刑冲({trigger_desc})。断语：羊刃叠叠，必主血光之灾，死于非命。",
            "probability": "高",
            "trigger_type": "DY" if has_dy_trigger and not has_ln_trigger else ("LN" if has_ln_trigger and not has_dy_trigger else "BOTH"),
            "dy_name": processed_pillars[4]['ganZhi']
        })
        found_die_die = True

    # If Die Die was NOT found (meaning yr_count_org < 2), then we check for standard Feng Chong
    if not found_die_die:
        chong_triggers = [t for t in triggers if t['rel'] == '冲']
        if chong_triggers:
            t = chong_triggers[0]
            clash_desc = f"{t['zhi_ext']}与{t['zhi_org']}相冲"
            
            # Check for Seven Killings (Qi Sha) - Must be ROOTED
            qi_sha_stems = [p['gan'] for p in processed_pillars if '杀' in p.get('tenGod', '')]
            has_rooted_qi_sha = False
            # Re-define LOCAL_WX just in case
            LOCAL_WX = {
                '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
                '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
                '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土',
                '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金',
                '戌': '土', '亥': '水'
            }
            
            for qi_gan in qi_sha_stems:
                s_wx = LOCAL_WX.get(qi_gan)
                if s_wx:
                    for p in processed_pillars:
                        for h in p['hidden']:
                            if h.get('gan') and LOCAL_WX.get(h.get('gan')) == s_wx:
                                has_rooted_qi_sha = True
                                break
                        if has_rooted_qi_sha: break
                if has_rooted_qi_sha: break
                
            if has_rooted_qi_sha:
                results.append({
                    "title": f"羊刃逢冲加七杀 {source}",
                    "description": f"原局羊刃背景下岁运引发冲局({clash_desc})，且杀刃相见(七杀有根)。断语：羊刃逢冲加七杀，必死无疑。",
                    "probability": "极高",
                    "trigger_type": "DY" if has_dy_trigger and not has_ln_trigger else ("LN" if has_ln_trigger and not has_dy_trigger else "BOTH"),
                    "dy_name": processed_pillars[4]['ganZhi']
                })
            else:
                results.append({
                    "title": f"羊刃逢冲 {source}",
                    "description": f"原局羊刃背景下岁运引发冲局({clash_desc})。断语：羊刃逢冲，不死也疯。",
                    "probability": "高",
                    "trigger_type": "DY" if has_dy_trigger and not has_ln_trigger else ("LN" if has_ln_trigger and not has_dy_trigger else "BOTH"),
                    "dy_name": processed_pillars[4]['ganZhi']
                })
            
    # Deduplicate
    seen_titles = set()
    final_res = []
    for r in results:
        if r['title'] not in seen_titles:
            seen_titles.add(r['title'])
            final_res.append(r)
            
    return final_res

def check_owl_devours_eating_god_logic(processed_pillars):
    """
    Renamed from 'check_eating_god_meets_owl' to be explicit.
    Now uses '枭神夺食' (Owl Devours Food) terminology.
    """
    # Define local WX mapping to avoid scope issues
    LOCAL_WX = {
        '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
        '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
        '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土',
        '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金',
        '戌': '土', '亥': '水'
    }

    results = []
    intra_branch_results = []
    
    # Helper to clean Ten God string (remove suffix if any, though bazi_logic uses single char usually '食' or '枭')
    # bazi_logic returns '食', '枭', '印', '比', etc.
    
    stems_ten_gods = [p['tenGod'] for p in processed_pillars]
    branches_ten_gods = [] # Main Qi checks
    # For Main Qi, we check the first hidden stem or calculate logic. 
    # bazi_logic passes hidden stems list. Usually first is Main Qi.
    # But simpler: processed_pillars doesn't strictly label Main Qi. 
    # Let's check Hidden Stems for presence.
    
    # Gather all existence
    has_eating_god_anywhere = False
    has_owl_anywhere = False
    
    eating_god_branches = [] # Indices of branches containing Eating God
    owl_branches = [] # Indices of branches containing Owl
    
    # Keywords
    eating_keywords = ['食', '食神']
    owl_keywords = ['枭', '偏印']

    for idx, p in enumerate(processed_pillars):
        # Check Stem
        stem_god = p.get('tenGod', '')
        if any(kw in stem_god for kw in eating_keywords): has_eating_god_anywhere = True
        if any(kw in stem_god for kw in owl_keywords): has_owl_anywhere = True
        
        # Check Branch (Hidden)
        branch_has_食 = False
        branch_has_枭 = False
        for h in p['hidden']:
            h_god = h.get('god', '')
            if any(kw in h_god for kw in eating_keywords): 
                branch_has_食 = True
                has_eating_god_anywhere = True
            if any(kw in h_god for kw in owl_keywords): 
                branch_has_枭 = True
                has_owl_anywhere = True
        
        if branch_has_食: eating_god_branches.append(idx)
        if branch_has_枭: owl_branches.append(idx)
        

        
            
        if branch_has_食 and branch_has_枭:
            source = "(原局)" if idx < 4 else "(岁运)"
            intra_branch_results.append({
                "title": f"枭神夺食 (同宫) {source}",
                "description": f"{p['zhi']}支藏干中同时包含食神与枭神(偏印)。",
                "probability": "高",
                "trigger_type": "DY" if idx == 4 else ("LN" if idx == 5 else "ORIGINAL"),
                "dy_name": processed_pillars[4]['ganZhi']
            })
            
    # Rule 1: Stem Interaction (Original adjacent OR External) + Rooted + No Wealth
    
    eating_indices = [i for i, x in enumerate(stems_ten_gods) if any(kw in x for kw in eating_keywords)]
    owl_indices = [i for i, x in enumerate(stems_ten_gods) if any(kw in x for kw in owl_keywords)]
    
    # Helper to check roots for a specific stem index (defined above, LOCAL_WX defined)
    def is_stem_rooted(idx, pillars):
        if idx >= len(pillars): return False
        stem_val = pillars[idx]['gan']
        stem_wx = LOCAL_WX.get(stem_val)
        if not stem_wx: return False
        for p in pillars:
            for h in p['hidden']:
                h_gan = h.get('gan')
                if h_gan and LOCAL_WX.get(h_gan) == stem_wx:
                    return True
        return False

    hits = [] # Store all findings: {desc, indices, rule_name}

    # --- Rule 1: Stem Interaction (Ten Gods) ---
    eating_rooted = any(is_stem_rooted(i, processed_pillars) for i in eating_indices)
    owl_rooted = any(is_stem_rooted(i, processed_pillars) for i in owl_indices)
    
    if eating_rooted and owl_rooted:
        r1_found = False
        r1_indices = []
        for e_idx in eating_indices:
            for o_idx in owl_indices:
                is_original = (e_idx < 4 and o_idx < 4)
                is_adjacent = abs(e_idx - o_idx) == 1
                if not is_original or is_adjacent:
                    r1_found = True
                    r1_indices = [e_idx, o_idx]
                    break
            if r1_found: break
        
        if r1_found:
            cai_indices = [i for i, x in enumerate(stems_ten_gods) if '财' in x]
            cai_rooted = any(is_stem_rooted(i, processed_pillars) for i in cai_indices)
            if not cai_rooted:
                 hits.append({
                     'desc': "天干食神与枭神相见(且有根)，无财星护卫",
                     'indices': r1_indices,
                     'rule': '天干'
                 })

    # --- Rule 2: Same Pillar (Tong Zhu) ---
    # Logic implies check p['hidden'] for Eating God
    for idx, p in enumerate(processed_pillars):
        stem_god = p.get('tenGod', '')
        if any(kw in stem_god for kw in owl_keywords):
             hidden_gods = [h['god'] for h in p['hidden']]
             if any(kw in hg for hg in hidden_gods for kw in eating_keywords):
                 hits.append({
                     'desc': f"{p['gan']}{p['zhi']}同柱：枭神盖头克食神",
                     'indices': [idx],
                     'rule': '同柱'
                 })

    # Rule 5: Owl Bureau (San He / San Hui)
    branches = [p['zhi'] for p in processed_pillars]
    
    # San He
    san_he_groups = [
        {'申', '子', '辰'}, {'亥', '卯', '未'}, 
        {'寅', '午', '戌'}, {'巳', '酉', '丑'}
    ]
    # San Hui
    san_hui_groups = [
        {'亥', '子', '丑'}, {'寅', '卯', '辰'},
        {'巳', '午', '未'}, {'申', '酉', '戌'}
    ]
    
    # Get Day Master Element
    dm_stem = processed_pillars[2]['gan']
    dm_wx = LOCAL_WX.get(dm_stem)
    
    # Calculate Resource Element
    resource_map = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
    resource_wx = resource_map.get(dm_wx)
    
    bureau_map = {
        frozenset(['申', '子', '辰']): '水', frozenset(['亥', '卯', '未']): '木',
        frozenset(['寅', '午', '戌']): '火', frozenset(['巳', '酉', '丑']): '金',
        frozenset(['亥', '子', '丑']): '水', frozenset(['寅', '卯', '辰']): '木',
        frozenset(['巳', '午', '未']): '火', frozenset(['申', '酉', '戌']): '金'
    }
    
    b_set = set(branches)
    
    for group, element in bureau_map.items():
        if group.issubset(b_set):
            if element == resource_wx:
                if has_eating_god_anywhere:
                    # Determine trigger type for Bureau
                    # If bureau involves indices 4 or 5
                    b_indices = [i for i, b in enumerate(branches) if b in group]
                    has_dy = 4 in b_indices
                    has_ln = 5 in b_indices
                    t_type = "DY" if has_dy and not has_ln else ("LN" if has_ln and not has_dy else ("BOTH" if has_dy or has_ln else "ORIGINAL"))
                    
                    hits.append({
                        'desc': f"地支成{element}局(印/枭局)，且命局有食神。",
                        'indices': b_indices,
                        'rule': '三合/三会'
                    })

    # --- Consolidate Hits (Rule 1, 2, 5) ---
    # Separate into Static and Dynamic
    static_hits = []
    dynamic_hits = []
    
    for h in hits:
        indices = h.get('indices', [])
        is_dynamic = any(i >= 4 for i in indices)
        if is_dynamic:
            dynamic_hits.append(h)
        else:
            static_hits.append(h)
            
    # Create ONE result for Static
    if static_hits:
        desc_list = [h['desc'] for h in static_hits]
        full_desc = "；".join(desc_list) + "。断语：食神逢枭，十有九死伤；食神遇枭，尸逢道路旁。"
        results.append({
            "title": "枭神夺食 (原局)",
            "description": full_desc,
            "probability": "高",
            "trigger_type": "ORIGINAL",
            "dy_name": processed_pillars[4]['ganZhi']
        })
        
    # Create ONE result for Dynamic (Sui Yun)
    if dynamic_hits:
        desc_list = [h['desc'] for h in dynamic_hits]
        full_desc = "；".join(desc_list) + "。断语：食神逢枭，十有九死伤；食神遇枭，尸逢道路旁。"
        
        # Determine overall trigger type based on ALL dynamic hits
        all_indices = []
        for h in dynamic_hits:
            all_indices.extend(h['indices'])
        
        has_dy = 4 in all_indices
        has_ln = 5 in all_indices
        
        t_type = "DY" if has_dy and not has_ln else ("LN" if has_ln and not has_dy else "BOTH")
        
        results.append({
            "title": "枭神夺食 (岁运引动)",
            "description": full_desc,
            "probability": "高",
            "trigger_type": t_type,
            "dy_name": processed_pillars[4]['ganZhi']
        })
        
    # Add Intra-Branch Results (Rule 4) - Already processed
    results.extend(intra_branch_results)
            
    # Deduplicate by Title
    seen_titles = set()
    final_res = []
    for r in results:
        # Key by title AND trigger_type to allow separate DY/LN alerts if titles same (though titles differ by suffix)
        key = (r['title'], r['trigger_type']) 
        if key not in seen_titles:
            seen_titles.add(key)
            final_res.append(r)
            
    return final_res
