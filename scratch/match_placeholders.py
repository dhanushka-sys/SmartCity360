import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

print("=== TABLE 0 (Figures Table) ===")
for r_idx, row in enumerate(doc.tables[0].rows):
    cells = [c.text.strip().replace('\n', ' ') for c in row.cells]
    print(f"Row {r_idx}: {cells}")

print("\n=== PLACEHOLDER TABLES ===")
for t_idx in range(2, 21):
    table = doc.tables[t_idx]
    first_cell_text = table.rows[0].cells[0].text
    lines = [line.strip() for line in first_cell_text.split('\n') if line.strip()]
    header = lines[0] if lines else "EMPTY"
    title = lines[1] if len(lines) > 1 else ""
    print(f"Table {t_idx:2d} -> {header} | {title}")

