import os
from PIL import Image

src = r"C:\Users\Bhoja\.gemini\antigravity-ide\brain\9631d371-d768-4926-9544-c2d16872742b\media__1782631806718.jpg"
dest_base = r"D:\panchapeetas-mobile\app\src\main\res"

sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192
}

try:
    img = Image.open(src)
    # Ensure it's in RGBA for PNG
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    for folder, size in sizes.items():
        folder_path = os.path.join(dest_base, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Save as ic_launcher.png
        resized_img.save(os.path.join(folder_path, "ic_launcher.png"), "PNG")
        # Save as ic_launcher_round.png
        resized_img.save(os.path.join(folder_path, "ic_launcher_round.png"), "PNG")
    print("Icons successfully generated and copied.")
except Exception as e:
    print("Error:", e)
