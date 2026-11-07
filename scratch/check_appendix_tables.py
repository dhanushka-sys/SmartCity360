import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

for idx in [24, 25, 26, 48, 49]:
    t = doc.tables[idx]
    print(f"\n=== Table {idx} ===")
    print(t.rows[0].cells[0].text[:300])

