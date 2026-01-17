from lunar_python import Lunar

try:
    print("Testing 3 args...")
    l = Lunar.fromYmd(2023, 2, 15)
    print(f"3 args OK: {l}")
except Exception as e:
    print(f"3 args Failed: {e}")

try:
    print("Testing 4 args (Leap)...")
    l = Lunar.fromYmd(2023, 2, 15, True)
    print(f"4 args OK: {l}")
except Exception as e:
    print(f"4 args Failed: {e}")
    
# Check Solar Conversion
l = Lunar.fromYmd(2023, 2, 15)
s = l.getSolar()
print(f"Solar: {s.getYear()}-{s.getMonth()}-{s.getDay()}")
