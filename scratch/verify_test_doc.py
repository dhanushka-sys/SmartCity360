import docx

doc = docx.Document(r"scratch\test_doc.docx")
table = doc.tables[2]
print(f"Cell paragraphs count: {len(table.rows[0].cells[0].paragraphs)}")
for idx, p in enumerate(table.rows[0].cells[0].paragraphs):
    print(f"P[{idx}]: {p.text[:60]} (runs: {len(p.runs)})")
    for r in p.runs:
        if r._r.xpath('.//a:blip'):
            print(f"   -> Contains inline image! {r._r.xpath('.//a:blip/@r:embed')}")

