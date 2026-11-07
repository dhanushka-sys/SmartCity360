import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

print("--- Searching in Tables ---")
for t_idx, table in enumerate(doc.tables):
    for r_idx, row in enumerate(table.rows):
        for c_idx, cell in enumerate(row.cells):
            txt = cell.text.strip()
            if "PLACEHOLDER" in txt.upper() or "📷" in txt or "FIGURE" in txt.upper():
                for p in cell.paragraphs:
                    p_txt = p.text.strip()
                    if "PLACEHOLDER" in p_txt.upper() or "📷" in p_txt or ("FIGURE" in p_txt.upper() and any(k in p_txt for k in ["2.", "3.", "4.", "5.", "6.", "7."])):
                        print(f"Table[{t_idx}] Row[{r_idx}] Cell[{c_idx}]: {p_txt[:120]}")

print("--- Searching in Paragraphs ---")
for idx, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if "PLACEHOLDER" in txt.upper() or "📷" in txt:
        print(f"P[{idx}]: {txt[:120]}")

