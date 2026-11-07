import docx

doc = docx.Document(r"scratch\test_clean_doc.docx")
table = doc.tables[2]
cell = table.rows[0].cells[0]
p = cell.paragraphs[0]
for idx, r in enumerate(p.runs):
    print(f"Run {idx}: text={repr(r.text)}, blip={bool(r._r.xpath('.//a:blip'))}")

