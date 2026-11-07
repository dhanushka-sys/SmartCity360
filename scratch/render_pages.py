import pymupdf
import os

doc = pymupdf.open(r"scratch/current.pdf")
os.makedirs("scratch/pdf_pages", exist_ok=True)

# Let's render a selection of pages:
# Page 1 (Title), Page 2-3 (TOC), Page 5 (Section 2 with Figure 2.1), Page 6 (Figure 2.2 and Listing 2.1),
# and some Appendix pages (Page 44, 45, 46)
pages_to_render = [0, 1, 4, 5, 8, 9, 43, 44, 45]

for p_no in pages_to_render:
    if p_no < len(doc):
        page = doc[p_no]
        pix = page.get_pixmap(dpi=150)
        out_path = f"scratch/pdf_pages/page_{p_no + 1}.png"
        pix.save(out_path)
        print(f"Rendered Page {p_no + 1}: {out_path} ({pix.width}x{pix.height})")

