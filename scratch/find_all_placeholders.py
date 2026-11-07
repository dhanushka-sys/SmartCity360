import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

print("=== PARAGRAPHS WITH 'PLACEHOLDER' ===")
for idx, p in enumerate(doc.paragraphs):
    if "PLACEHOLDER" in p.text.upper():
        print(f"P[{idx}]: {p.text}")

print("\n=== TABLES WITH 'PLACEHOLDER' ===")
for t_idx, t in enumerate(doc.tables):
    for r_idx, r in enumerate(t.rows):
        for c_idx, c in enumerate(r.cells):
            if "PLACEHOLDER" in c.text.upper():
                print(f"Table[{t_idx}] R[{r_idx}] C[{c_idx}]: {c.text.split(chr(10))[0]}")

