import docx

doc = docx.Document(r"scratch\test_clean_doc.docx")
table = doc.tables[2]
cell = table.rows[0].cells[0]

print(f"Number of paragraphs in Table 2: {len(cell.paragraphs)}")
p = cell.paragraphs[0]
print(f"P[0] text: repr({p.text})")
print(f"P[0] runs: {len(p.runs)}")
print(f"Has picture: {bool(p.runs[0]._r.xpath('.//a:blip'))}")

# Check surrounding text
parent = table._tbl.getparent()
idx = parent.index(table._tbl)
prev_p = docx.text.paragraph.Paragraph(parent[idx-1], doc)
next_p = docx.text.paragraph.Paragraph(parent[idx+1], doc)

print(f"PREV P: {prev_p.text[:70]}")
print(f"TABLE 2: [Clean 6.2\" Image]")
print(f"NEXT P: {next_p.text[:70]}")

