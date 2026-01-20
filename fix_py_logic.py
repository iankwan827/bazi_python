
import os

file_path = r"e:\SD\bazi - 副本\bazi_python\life_death_analysis.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Secret 25 to Merged Version
s25_start = "# Secret 25: 卧室风水 (床下物件)"
s25_end_marker = "# Deduplicate" # It's followed by this

if s25_start in content:
    start_idx = content.find(s25_start)
    end_idx = content.find(s25_end_marker, start_idx)
    
    if start_idx != -1 and end_idx != -1:
        new_s25 = """# Secret 25: 卧室风水 (床下物件) - Merged
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
            '正官': '重要工作资料', '七杀': '尖锐危险物品',
            '正财': '贵重物品收纳盒', '偏财': '杂物堆积，杂乱无章',
            '正印': '书籍或相册', '偏印': '过期药品',
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
                combined_desc.append(f"{item['name']}：{zhi}({main_qi_god or '无藏干'})。床下/卧室隐蔽处可能有：{desc_str}。")

        if combined_desc:
            all_results.append({
                'title': "秘诀：卧室风水",
                'description': "<br/>".join(combined_desc),
                'probability': "中",
                'trigger_type': 'ORIGINAL',
                'category': 'INFO'
            })
            
    # Set default for new ones too
    for r in all_results:
        if 'category' not in r: r['category'] = 'RISK'

    """
        content = content[:start_idx] + new_s25 + content[end_idx:]
    else:
        print("Could not find S25 range")
else:
    print("S25 Start not found")

# 2. Inject Categories for specific items
# Secret 24 (Moles) -> INFO
target_s24 = "'trigger_type': 'ORIGINAL'"
replacement_s24 = "'trigger_type': 'ORIGINAL',\n                'category': 'INFO'"
# We only want to replace it inside Secret 24 block.
s24_marker = "# Secret 24: 月支断痣"
if s24_marker in content:
    s24_idx = content.find(s24_marker)
    # Find the next trigger_type after this marker
    tt_idx = content.find(target_s24, s24_idx)
    # But be careful not to replace others.
    # Actually, simpler: just regex replace based on title?
    pass # Let's stick to simple string manipulation if unique.

# Actually, the easier way is to inject specific categories by Title keyword in the "Set default" loop I added above!
# But I added that loop at the end (inside the new S25 block).
# Let's modify the new_s25 block to handle overrides.

new_s25_v2 = """# Secret 25: 卧室风水 (床下物件) - Merged
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
            '正官': '重要工作资料', '七杀': '尖锐危险物品',
            '正财': '贵重物品收纳盒', '偏财': '杂物堆积，杂乱无章',
            '正印': '书籍或相册', '偏印': '过期药品',
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
                combined_desc.append(f"{item['name']}：{zhi}({main_qi_god or '无藏干'})。床下/卧室隐蔽处可能有：{desc_str}。")

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

    """

# Re-apply replacement with v2 logic
if s25_start in content:
    start_idx = content.find(s25_start)
    end_idx = content.find(s25_end_marker, start_idx)
    if start_idx != -1 and end_idx != -1:
         content = content[:start_idx] + new_s25_v2 + content[end_idx:]

# 3. Add Sorting
# Find return statement
return_stmt = "return unique_results"
if return_stmt in content:
    # Add sorting before return
    sort_logic = """
    # Sort
    cat_order = {'RISK': 1, 'GOOD': 2, 'INFO': 3}
    unique_results.sort(key=lambda x: cat_order.get(x.get('category', 'RISK'), 99))
            
    """
    content = content.replace(return_stmt, sort_logic + return_stmt)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated life_death_analysis.py successfully")
