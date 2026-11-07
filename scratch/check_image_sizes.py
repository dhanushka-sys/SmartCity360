from PIL import Image
import glob

for img_path in sorted(glob.glob(r"scratch\slide_images\*.png")):
    with Image.open(img_path) as im:
        print(f"{img_path}: {im.size} (aspect ratio: {im.size[0]/im.size[1]:.2f})")

