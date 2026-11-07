from PIL import Image

im1 = Image.open(r"C:/Users/Dhanushka Maduranga/.gemini/antigravity/brain/0731c486-f798-497e-b236-2bb7f941f183/.user_uploaded/media_1794001135240_f3886161.png")
im2 = Image.open(r"C:/Users/Dhanushka Maduranga/.gemini/antigravity/brain/0731c486-f798-497e-b236-2bb7f941f183/.user_uploaded/media_1794001084914_965f4c95.jpg")

print(f"im1 (StreamData): size={im1.size}, mode={im1.mode}")
print(f"im2 (EnergyStreamData): size={im2.size}, mode={im2.mode}")

# Sample top colors of im1
for y in range(0, 35, 5):
    print(f"y={y}: x=10 -> {im1.getpixel((10, y))}, x=50 -> {im1.getpixel((50, y))}, x=200 -> {im1.getpixel((200, y))}")

# Sample background color in editor area
print(f"Editor bg: x=300, y=100 -> {im1.getpixel((300, 100))}")
print(f"Gutter bg: x=20, y=100 -> {im1.getpixel((20, 100))}")

