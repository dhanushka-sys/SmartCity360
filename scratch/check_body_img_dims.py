from PIL import Image
import os
import docx

doc = docx.Document(r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx")

print("=== MAIN BODY FIGURES & LISTINGS (TABLES 2 TO 20) ===")
for idx in range(2, 21):
    tbl = doc.tables[idx]
    cell = tbl.cell(0, 0)
    blips = cell._element.xpath('.//a:blip/@r:embed')
    for b in blips:
        part = doc.part.related_parts[b]
        # read image bytes with PIL
        import io
        im = Image.open(io.BytesIO(part.blob))
        print(f"Table {idx:2d}: {im.size[0]}x{im.size[1]} | aspect: {im.size[0]/im.size[1]:.2f}")

