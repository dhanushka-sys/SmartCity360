import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

print("--- FIGURE TABLES (e.g. Table 2) ---")
for t_idx in [2, 3, 5]:
    table = doc.tables[t_idx]
    print(f"\n=== Table {t_idx} ===")
    for p in table.rows[0].cells[0].paragraphs:
        if p.text.strip():
            print(f"P: {p.text[:120]}")

print("\n--- CODE SCREENSHOT TABLES (e.g. Table 4, 7) ---")
for t_idx in [4, 7]:
    table = doc.tables[t_idx]
    print(f"\n=== Table {t_idx} ===")
    for p in table.rows[0].cells[0].paragraphs:
        if p.text.strip():
            print(f"P: {p.text[:120]}")

