import pymupdf

doc = pymupdf.open(r"scratch/current.pdf")
page = doc[9] # 0-based page 10
pix = page.get_pixmap(dpi=150)
pix.save("scratch/pdf_pages/page_10.png")

