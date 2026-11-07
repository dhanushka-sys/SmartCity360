import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

p = doc.paragraphs[0]
print(f"P[0] style: {p.style.name}")
for r in p.runs:
    print(f"Run: font={r.font.name}, size={r.font.size}, color={r.font.color.rgb if r.font.color else None}, bold={r.bold}")

table = doc.tables[2]
p_cell = table.rows[0].cells[0].paragraphs[0]
print(f"Cell P style: {p_cell.style.name}")
for r in p_cell.runs:
    print(f"Cell Run: font={r.font.name}, size={r.font.size}, color={r.font.color.rgb if r.font.color else None}, bold={r.bold}")

