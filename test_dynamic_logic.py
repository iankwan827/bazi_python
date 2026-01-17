from bazi_logic import get_dynamic_interactions

# Dummy Pillar
# 4 Pillars: Jia Zi, Yi Chou, Bing Yin, Ding Mao
# DY: Wu Chen (index 4)
# LN: Ji Si (index 5)

# Expected:
# Zi (0) - Chen (4) -> Ban He Water
# Chou (1) - Si (5) -> Ban He Metal? Or San He part?
# Yin (2) - Si (5) -> Xing/Hai
# Mao (3) - Chen (4) -> Hai
# Chen (4) - Si (5) -> None direct?

pillars = [
    {'gan': '甲', 'zhi': '子'},
    {'gan': '乙', 'zhi': '丑'},
    {'gan': '丙', 'zhi': '寅'},
    {'gan': '丁', 'zhi': '卯'},
    {'gan': '戊', 'zhi': '辰'}, # DY
    {'gan': '己', 'zhi': '巳'}  # LN
]

print("Testing Dynamic Interactions...")
res = get_dynamic_interactions(pillars, [4, 5])

print("Stems:", res['stems'])
print("Branches:", res['branches'])
