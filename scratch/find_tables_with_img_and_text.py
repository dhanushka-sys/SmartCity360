import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

print("=== CHECKING ALL TABLES FOR (HAS_IMAGE and HAS_TEXT) ===")
for t_idx, table in enumerate(doc.tables):
    cell = table.rows[0].cells[0]
    
    # check image
    has_image = False
    for p in cell.paragraphs:
        for r in p.runs:
            if r._r.xpath('.//a:blip'):
                has_image = True
                break
                
    # check text
    texts = [p.text.strip() for p in cell.paragraphs if p.text.strip()]
    if has_image:
        print(f"Table {t_idx:2d}: HAS_IMAGE=True, text paragraphs={len(texts)}")
        if texts:
            for i, txt in enumerate(texts):
                print(f"   [{i}] {txt[:80]}")

