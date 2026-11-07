from PIL import Image, ImageDraw, ImageFont
import os

font_path = r"C:\Windows\Fonts\consola.ttf"
if not os.path.exists(font_path):
    font_path = r"C:\Windows\Fonts\cour.ttf"

font = ImageFont.truetype(font_path, 20)
im = Image.new("RGB", (400, 100), color=(30, 31, 34))
draw = ImageDraw.Draw(im)
draw.text((20, 30), "public class Test {", fill=(200, 200, 200), font=font)
im.save(r"scratch\test_pil.png")
print("Saved test_pil.png successfully!", os.path.getsize(r"scratch\test_pil.png"))

