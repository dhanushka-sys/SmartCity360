import pymupdf
import os

doc = pymupdf.open(r"scratch/fixed.pdf")
os.makedirs("scratch/fixed_pages", exist_ok=True)

pages_to_render = [0, 1, 3, 4, 9, 10, 48, 49, 50]

for p_no in pages_to_render:
    if p_no < len(doc):
        page = doc[p_no]
        pix = page.get_pixmap(dpi=150)
        out_path = f"scratch/fixed_pages/page_{p_no + 1}.png"
        pix.save(out_path)
        print(f"Rendered Page {p_no + 1}: {out_path}")

