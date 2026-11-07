import pymupdf

doc = pymupdf.open(r"scratch/before.pdf")

for p_no in range(46, min(51, len(doc))):
    page = doc[p_no]
    pix = page.get_pixmap(dpi=150)
    pix.save(f"scratch/pdf_pages/before_page_{p_no + 1}.png")
    print(f"Rendered before page {p_no + 1}")

