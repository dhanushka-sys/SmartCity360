import pymupdf
import os

doc = pymupdf.open(r"scratch/restored_old_design.pdf")
os.makedirs("scratch/restored_pages", exist_ok=True)

pages = [0, 4, 8, 10, 11, 45, 46, 47]

for p_no in pages:
    if p_no < len(doc):
        page = doc[p_no]
        pix = page.get_pixmap(dpi=150)
        pix.save(f"scratch/restored_pages/page_{p_no + 1}.png")
        print(f"Rendered Page {p_no + 1}")

