import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

for t_idx in [4, 7, 10, 13, 16]:
    table = doc.tables[t_idx]
    cell = table.rows[0].cells[0]
    print(f"\n=== Table {t_idx} (paragraphs: {len(cell.paragraphs)}) ===")
    for p in cell.paragraphs:
        print(f"  {repr(p.text[:80])}")

