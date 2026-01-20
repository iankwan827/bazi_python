import datetime
from bazi_logic import get_shen_sha, SHEN_SHA_RULES

def test_gu_luan_sha():
    print("Testing Gu Luan Sha...")
    
    # Test Cases for Gu Luan Sha (Day Pillar)
    # 乙巳, 丁巳, 辛亥, 戊申, 壬子
    
    test_cases = [
        ('乙', '巳', True),
        ('丁', '巳', True),
        ('辛', '亥', True),
        ('戊', '申', True),
        ('壬', '子', True),
        ('甲', '子', False), # Control
        ('乙', '卯', False), # Control
    ]
    
    for stem, zhi, expected in test_cases:
        # Mock info object
        info = {
            'yearGan': '甲', 'yearZhi': '子', 'monthZhi': '丑', 
            'dayGan': stem, 'dayZhi': zhi, 'stem': stem, 'zhi': zhi,
            'yearNaYin': '', 'dayNaYin': ''
        }
        
        # We can test the rule directly from the dictionary for precision
        rule = SHEN_SHA_RULES.get('孤鸾煞')
        if not rule:
            print("Error: '孤鸾煞' rule not found in SHEN_SHA_RULES")
            return

        result = rule(info)
        status = "PASS" if result == expected else "FAIL"
        print(f"Day Pillar {stem}{zhi}: Expected {expected}, Got {result} -> {status}")
    
    print("Test Complete.")

if __name__ == "__main__":
    test_gu_luan_sha()
