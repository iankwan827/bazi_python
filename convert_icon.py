from PIL import Image
import os

png_path = r"E:/Users/Administrator/.gemini/antigravity/brain/e1262423-a858-4e6e-ab1f-24e256d7672a/bazi_app_icon_1768455891123.png"
ico_path = os.path.join(os.getcwd(), "bazi.ico")

try:
    img = Image.open(png_path)
    # Resize to standard icon sizes
    img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"Successfully created {ico_path}")
except Exception as e:
    print(f"Error converting: {e}")
