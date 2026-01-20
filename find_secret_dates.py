
import datetime
from lunar_python import Solar
from bazi_logic import GAN, ZHI, HIDDEN_STEMS_MAP, TEN_GODS, NAYIN
from life_death_analysis import get_nayin_element, is_element_countering

def get_ten_god(day_gan, target_gan):
    key = day_gan + target_gan
    val = TEN_GODS.get(key)
    return val[0] if val else ''

def get_processed_pillars(solar):
    lunar = solar.getLunar()
    bazi = lunar.getEightChar()
    
    yg = bazi.getYearGan()
    yz = bazi.getYearZhi()
    mg = bazi.getMonthGan()
    mz = bazi.getMonthZhi()
    dg = bazi.getDayGan()
    dz = bazi.getDayZhi()
    hg = bazi.getTimeGan()
    hz = bazi.getTimeZhi()
    
    pg = [yg, mg, dg, hg]
    pz = [yz, mz, dz, hz]
    
    pillars = []
    day_gan = dg
    
    for i in range(4):
        gan = pg[i]
        zhi = pz[i]
        
        # Ten God for Stem
        tg = get_ten_god(day_gan, gan)
        
        # Hidden Stems
        hidden = []
        hidden_stems = HIDDEN_STEMS_MAP.get(zhi, [])
        for h_stem in hidden_stems:
            hidden.append({
                'stem': h_stem,
                'god': get_ten_god(day_gan, h_stem)
            })
            
        # Na Yin
        gz = gan + zhi
        ny = NAYIN.get(gz, '')
        
        pillars.append({
            'gan': gan,
            'zhi': zhi,
            'ganZhi': gz,
            'tenGod': tg,
            'hidden': hidden,
            'naYin': ny
        })
        
    return pillars

def find_secrets():
    start_date = datetime.date(1980, 1, 1)
    end_date = datetime.date(2030, 1, 1)
    delta = datetime.timedelta(days=1)
    
    found_secrets = {
        's1': [],
        's2': [],
        's3': [],
        's4': []
    }
    
    curr = start_date
    while curr < end_date:
        # Check noon 12:00
        solar = Solar.fromYmdHms(curr.year, curr.month, curr.day, 12, 0, 0)
        pillars = get_processed_pillars(solar)
        
        # S1: Year Bi, Month Bi, Hidden IW (PianCai/Cai), No Stem IW
        p0_ten = pillars[0]['tenGod']
        p1_ten = pillars[1]['tenGod']
        if '比' in p0_ten and '比' in p1_ten:
            stems_ten = [p['tenGod'] for p in pillars]
            has_iw_on_stem = any('才' in t or '偏财' in t for t in stems_ten)
            if not has_iw_on_stem:
                # Check Hidden
                hidden_iw = False
                for p in pillars:
                    for h in p['hidden']:
                        if '才' in h['god'] or '偏财' in h['god']:
                            hidden_iw = True
                            break
                    if hidden_iw: break
                
                if hidden_iw and len(found_secrets['s1']) < 3:
                     found_secrets['s1'].append(curr.isoformat())

        # S2: Year/Month Branch Main Qi is Direct Wealth (Zheng Cai/Cai - note short name '财' is usually Zheng Cai)
        # Main Qi is usually index 0 of hidden
        y_hidden = pillars[0]['hidden']
        m_hidden = pillars[1]['hidden']
        if y_hidden and m_hidden:
            y_main = y_hidden[0]['god']
            m_main = m_hidden[0]['god']
            # Strictly matches '正财' or '财'
            # Must NOT match '劫财' (Jie Cai) or '偏财' (Pian Cai)
            if (y_main == '财' or y_main == '正财') and \
               (m_main == '财' or m_main == '正财'):
                if len(found_secrets['s2']) < 3:
                    found_secrets['s2'].append(curr.isoformat())

        # S3: Year Hurting (Shang Guan/Shang), Month Owl (Pian Yin/Xiao)
        if ('伤' in p0_ten) and ('枭' in p1_ten or '偏印' in p1_ten):
             if len(found_secrets['s3']) < 3:
                 found_secrets['s3'].append(curr.isoformat())
                 
        # S4: Year Na Yin countered by Month Na Yin
        y_ny = get_nayin_element(pillars[0]['naYin'])
        m_ny = get_nayin_element(pillars[1]['naYin'])
        if y_ny and m_ny and is_element_countering(m_ny, y_ny):
             if len(found_secrets['s4']) < 3:
                 found_secrets['s4'].append(curr.isoformat())
        
        # Stop if all found
        if all(len(v) >= 1 for v in found_secrets.values()):
            # We want a few examples, maybe just break when we have 1 of each or scan a bit more?
            # Let's get 1 of each is fine, but prompt asked for "data" maybe plural.
            pass
        
        if all(len(v) >= 3 for v in found_secrets.values()):
            break
            
        curr += delta

    print("Found Dates:")
    print("--- Secret 1 (Bi Jian / Hidden IW) ---")
    for d in found_secrets['s1']: print(d)
    
    print("\n--- Secret 2 (Direct Wealth Main Qi) ---")
    for d in found_secrets['s2']: print(d)
    
    print("\n--- Secret 3 (Year Hurting / Month Owl) ---")
    for d in found_secrets['s3']: print(d)
    
    with open('verified_secrets.txt', 'w', encoding='utf-8') as f:
        f.write("Secret 1 (Bi Jian / Hidden IW): " + (found_secrets['s1'][0] if found_secrets['s1'] else "None") + "\n")
        f.write("Secret 2 (Direct Wealth Main Qi): " + (found_secrets['s2'][0] if found_secrets['s2'] else "None") + "\n")
        f.write("Secret 3 (Year Hurting / Month Owl): " + (found_secrets['s3'][0] if found_secrets['s3'] else "None") + "\n")
        f.write("Secret 4 (Na Yin Countering): " + (found_secrets['s4'][0] if found_secrets['s4'] else "None") + "\n")

if __name__ == '__main__':
    find_secrets()
