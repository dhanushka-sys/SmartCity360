import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

for t_idx in range(2, 21):
    table = doc.tables[t_idx]
    print(f"\n==================== TABLE {t_idx} ====================")
    for r_idx, row in enumerate(table.rows):
        for c_idx, cell in enumerate(row.cells):
            print(f"--- Row {r_idx}, Cell {c_idx} ---")
            for p in cell.paragraphs:
                print(p.text)

