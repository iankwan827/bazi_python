import sys
import os
import glob

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

scripts_dir = os.path.join(os.path.dirname(sys.executable), 'Scripts')
print(f"Scripts Directory: {scripts_dir}")

if os.path.exists(scripts_dir):
    print("Files in Scripts directory matching *deploy*:")
    for f in glob.glob(os.path.join(scripts_dir, "*deploy*")):
        print(f"  - {os.path.basename(f)}")
    for f in glob.glob(os.path.join(scripts_dir, "*pyside6*")):
        print(f"  - {os.path.basename(f)}")
else:
    print("Scripts directory does not exist!")

try:
    import PySide6
    print(f"PySide6 Version: {PySide6.__version__}")
    print(f"PySide6 Location: {os.path.dirname(PySide6.__file__)}")
except ImportError as e:
    print(f"Error importing PySide6: {e}")
