from lunar_python import Lunar

# 2023 has Leap 2nd Month
print("--- Test Leap Month Logic ---")
l1 = Lunar.fromYmd(2023, 2, 1)
print(f"Base: {l1.toString()} isLeap: {l1.isLeap()}")

# Get days in this month
days = l1.getDayCount()
print(f"Days in normal month: {days}")

# Move forward by that many days?
l2 = l1.next(days)
print(f"Next(days): {l2.toString()} isLeap: {l2.isLeap()}")

# Verify if it is indeed the Leap 2nd Month
if l2.getMonth() == 2 and l2.isLeap():
    print("SUCCESS: Found Leap Month!")
else:
    print("FAILURE: Did not land on Leap Month.")
