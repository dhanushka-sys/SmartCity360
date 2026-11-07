from PIL import Image
import os

appendix_dir = r"screenshots\appendix"
for f in sorted(os.listdir(appendix_dir)):
    if f.endswith('.png'):
        p = os.path.join(appendix_dir, f)
        im = Image.open(p)
        print(f"{f:35s}: {im.size[0]}x{im.size[1]} | aspect: {im.size[0]/im.size[1]:.2f}")

