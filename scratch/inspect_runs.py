import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")
cell = doc.tables[2].rows[0].cells[0]
p = cell.paragraphs[0]
print(f"Number of runs: {len(p.runs)}")
for idx, r in enumerate(p.runs):
    print(f"Run {idx}: text={repr(r.text[:50])}, bold={r.bold}, italic={r.italic}")

