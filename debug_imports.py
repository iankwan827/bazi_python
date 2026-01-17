import lunar_python
import sys

with open('debug_output.txt', 'w', encoding='utf-8') as f:
    f.write(str(dir(lunar_python)))
    f.write('\n\n')
    try:
        from lunar_python import Solar
        f.write("Solar import check: SUCCESS\n")
    except ImportError as e:
        f.write(f"Solar import check: FAILED - {e}\n")

    try:
        from lunar_python import Lunar
        f.write("Lunar import check: SUCCESS\n")
    except ImportError as e:
        f.write(f"Lunar import check: FAILED - {e}\n")
