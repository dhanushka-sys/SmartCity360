import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

for idx in range(24, 50):
    table = doc.tables[idx]
    cell = table.rows[0].cells[0]
    has_image = False
    for p in cell.paragraphs:
        for r in p.runs:
            if r._r.xpath('.//a:blip'):
                has_image = True
                break
    if has_image:
        print(f"Table {idx} has image!")

