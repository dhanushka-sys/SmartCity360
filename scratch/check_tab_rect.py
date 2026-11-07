from PIL import Image

im = Image.open(r"C:/Users/Dhanushka Maduranga/.gemini/antigravity/brain/0731c486-f798-497e-b236-2bb7f941f183/.user_uploaded/media_1794001135240_f3886161.png")

# Check tab rectangle dimensions in im
# Find where the tab starts and ends
for x in range(0, 300, 10):
    p = im.getpixel((x, 15))
    print(f"x={x}: {p[:3]}")

