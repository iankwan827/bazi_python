import json
from lunar_python import Solar

def generate_map():
    # Range: 1900 to 2100
    start_year = 1900
    end_year = 2100
    
    # Map: "JiaZi" -> [1924, 1984, 2044]
    year_map = {}
    
    for y in range(start_year, end_year + 1):
        # Use mid-year (June 15) to ensure we are safely inside the GanZhi year 
        # (LiChun is usually Feb 4)
        lunar = Solar.fromYmd(y, 6, 15).getLunar()
        gz = lunar.getYearInGanZhi()
        
        if gz not in year_map:
            year_map[gz] = []
        year_map[gz].append(y)
        
    # Write to file
    with open("year_map.json", "w", encoding="utf-8") as f:
        json.dump(year_map, f, ensure_ascii=False, indent=2)
        
    print(f"Generated map for {len(year_map)} pillars.")

if __name__ == "__main__":
    generate_map()
