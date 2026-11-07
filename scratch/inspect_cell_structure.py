import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")
table = doc.tables[2]
cell = table.rows[0].cells[0]

print(f"Cell has {len(cell.paragraphs)} paragraphs:")
for idx, p in enumerate(cell.paragraphs):
    print(f"P[{idx}]: {p.text}")

