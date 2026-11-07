import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

for idx, table in enumerate(doc.tables):
    first_row_text = " | ".join([c.text.strip().replace('\n', ' ') for c in table.rows[0].cells])
    print(f"Table {idx:2d}: rows={len(table.rows)}, cols={len(table.columns)} | {first_row_text[:90]}")

