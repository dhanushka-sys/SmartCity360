import pymupdf

doc = pymupdf.open(r"scratch/current.pdf")

for p_no in [44, 45, 46, 47, 48]:
    page = doc[p_no]
    pix = page.get_pixmap(dpi=150)
    out_path = f"scratch/pdf_pages/page_{p_no + 1}.png"
    pix.save(out_path)
    print(f"Rendered Page {p_no + 1}")

