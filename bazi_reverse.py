from lunar_python import Solar, Lunar
import datetime

GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

def validate_gan_zhi(gan, zhi):
    """Simple check if GanZhi pair is valid (odd-odd, even-even)"""
    if gan not in GAN or zhi not in ZHI: return False
    return GAN.index(gan) % 2 == ZHI.index(zhi) % 2

def find_date_from_bazi(year_gan, year_zhi, month_gan, month_zhi, day_gan, day_zhi, time_gan, time_zhi, ref_year):
    """
    Reverse lookup for Bazi.
    Args:
        year_gan, year_zhi: Year Pillar
        month_gan, month_zhi: Month Pillar
        day_gan, day_zhi: Day Pillar
        time_gan, time_zhi: Time Pillar (Gan is optional actually, determinable, but user inputs it)
        ref_year: A reference year (e.g., 2024, 1990) to search around. 
                  The algorithm searches for the closest matching Year Pillar nearby.
    Returns:
        Solar object of the match (Time set to middle of the hour period) or None.
    """
    
    # 1. Validate Input Basics
    if not (validate_gan_zhi(year_gan, year_zhi) and validate_gan_zhi(month_gan, month_zhi) and 
            validate_gan_zhi(day_gan, day_zhi) and validate_gan_zhi(time_gan, time_zhi)):
        print("Invalid GanZhi polarity")
        # return None # Soft fail or hard fail? Let's try to search anyway in case custom logic differs, strictly speaking this is physics.
        # But if the user inputs weird stuff, it won't be found regardless.
        
    # 2. Find Candidate Year
    # The Year Pillar (Jia Zi) repeats every 60 years.
    # We find the specific year 'y' close to ref_year that has this Year Pillar.
    # To be precise, Bazi year starts at LiChun.
    # We check the GanZhi of the LiChun of ref_year.
    
    # Simple strategy: Iterate ref_year - 65 to ref_year + 65 (covers >2 cycles just in case)
    # Actually just closest one is enough.
    
    target_year_gz = year_gan + year_zhi
    # Load pre-calculated map
    import json
    import os
    
    map_path = os.path.join(os.path.dirname(__file__), "year_map.json")
    try:
        with open(map_path, "r", encoding="utf-8") as f:
            YEAR_MAP = json.load(f)
    except FileNotFoundError:
        print("Warning: year_map.json not found. Falling back to slow search.")
        YEAR_MAP = None

    target_ygz = year_gan + year_zhi
    candidate_years = []
    
    if YEAR_MAP and target_ygz in YEAR_MAP:
        # Fast Lookup
        all_years = YEAR_MAP[target_ygz]
        # Filter by range +/- 100
        for y in all_years:
            if ref_year - 100 <= y <= ref_year + 100:
                candidate_years.append(y)
    else:
        # Fallback Slow Search
        for y in range(ref_year - 100, ref_year + 100):
            lunar = Solar.fromYmd(y, 6, 15).getLunar()
            gz = lunar.getYearInGanZhi()
            if gz == target_ygz:
                 candidate_years.append(y)
    
    # If no years found
    if not candidate_years:
        return []
        
    # Sort candidates by proximity to ref_year
    candidate_years.sort(key=lambda x: abs(x - ref_year))
    
    found_results = []
    
    for y in candidate_years:
        # Search days in this year.
        # Range: Bazi year overlaps Gregorian. LiChun(y) to LiChun(y+1).
        # We search roughly Jan 1 of y to Feb 20 of y+1 to be safe.
        
        start_date = datetime.date(y, 1, 1)
        end_date = datetime.date(y + 1, 2, 20)
        delta = end_date - start_date
        
        for i in range(delta.days + 1):
            curr = start_date + datetime.timedelta(days=i)
            # Create Solar
            # Default to 12:00 PM for Day check
            solar_check = Solar.fromYmd(curr.year, curr.month, curr.day)
            lunar_check = solar_check.getLunar()
            bazi = lunar_check.getEightChar()
            
            # Match Year (re-verify strictly)
            if bazi.getYearGan() != year_gan or bazi.getYearZhi() != year_zhi:
                continue
                
            # Match Month
            if bazi.getMonthGan() != month_gan or bazi.getMonthZhi() != month_zhi:
                continue
                
            # Match Day
            if bazi.getDayGan() != day_gan or bazi.getDayZhi() != day_zhi:
                continue
                
            # Match Time
            # Found Day! Now check if Time is consistent.
            # Time Gan is derived from Day Gan + Time Zhi.
            # We can verify if the user's input Time Gan is correct for this Day Gan + Time Zhi.
            # But the primary search key is Time Zhi for the hour.
            
            # Calculate expected Time Gan
            # Day Gan Index
            day_gan_idx = GAN.index(day_gan) 
            # (d_idx % 5) * 2 -> starting gan for Zi hour
            start_gan_idx = (day_gan_idx % 5) * 2
            
            time_zhi_idx = ZHI.index(time_zhi)
            expected_time_gan_idx = (start_gan_idx + time_zhi_idx) % 10
            expected_time_gan = GAN[expected_time_gan_idx]
            
            if expected_time_gan != time_gan:
                # User input Time Gan mismatch? 
                # Strict mode: Fail.
                # Relaxed mode: Ignore Gan, trust Zhi?
                # User provided full 8 chars. If physics mismatch, it's invalid input.
                # Let's assume strict.
                continue
                
            # Construct Final Solar Date
            # Midpoint of the Double Hour
            # mid-point of the hour:
            # Zi (0): 00:00 (Safe)
            # Chou (1): 02:00 (1*2)
            # Yin (2): 04:00 (2*2)
            # ...
            # Hai (11): 22:00 (11*2)
            hour_try = ZHI.index(time_zhi) * 2

            
            # Simple check:
            if time_zhi == '子': hour_try = 0
            # For others, idx*2 is perfectly in the middle/start of the new day portion.
            
            solar_final = Solar.fromYmdHms(curr.year, curr.month, curr.day, hour_try, 0, 0)
            
            # Re-verify full chart
            bazi_final = solar_final.getLunar().getEightChar()
            if (bazi_final.getTimeGan() == time_gan and bazi_final.getTimeZhi() == time_zhi and
                bazi_final.getDayGan() == day_gan and bazi_final.getDayZhi() == day_zhi):
                found_results.append(solar_final)
                
        # If we found matches in this year, we continue to next year to find ALL matches?
        # Or stop? User wants 3-4 options. 
        # Usually checking all candidate years is safer.
        
    return found_results

if __name__ == "__main__":
    print("Testing Reverse Lookup...")
    # Test case: 2026-01-17 10:30 -> Yi Si Year
    # Gan: Yi, Zhi: Si
    # Month: Ji Chou
    # Day: Xin Mao
    # Time: Gui Si
    results = find_date_from_bazi('乙', '巳', '己', '丑', '辛', '卯', '癸', '巳', 2026)
    print(f"Results found: {len(results)}")
    for r in results:
        print(f"  {r.toFullString()}")

