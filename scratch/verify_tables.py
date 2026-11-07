import docx

doc_path = r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx"
doc = docx.Document(doc_path)

print(f"Total tables: {len(doc.tables)}")
for idx, table in enumerate(doc.tables):
    for r_i, row in enumerate(table.rows):
        for c_i, cell in enumerate(row.cells):
            has_pics = any(run._element.xpath('.//a:blip') for p in cell.paragraphs for run in p.runs)
            texts = [p.text.strip() for p in cell.paragraphs if p.text.strip()]
            if has_pics:
                print(f"Table {idx} [{r_i},{c_i}]: has_picture=True, num_paragraphs={len(cell.paragraphs)}, text_paragraphs={texts}")
            elif texts:
                # print summary if it looks like a listing or figure
                for t in texts:
                    if "LISTING" in t or "FIGURE" in t or "SOURCE CODE" in t or "DIAGRAM" in t:
                        print(f"Table {idx} [{r_i},{c_i}]: TEXT CONTAINS PLACEHOLDER KEYWORD: {t[:80]}")

