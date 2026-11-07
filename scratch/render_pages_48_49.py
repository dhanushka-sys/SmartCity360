import pymupdf

doc = pymupdf.open(r"scratch/fixed.pdf")

for p_no in [47, 48]: # pages 48 and 49
    page = doc[p_no]
    pix = page.get_pixmap(dpi=150)
    out_path = f"scratch/fixed_pages/page_{p_no + 1}.png"
    pix.save(out_path)
    print(f"Rendered Page {p_no + 1}")

