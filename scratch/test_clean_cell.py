import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

table = doc.tables[2]
cell = table.rows[0].cells[0]

print(f"Current paragraphs in Table 2: {len(cell.paragraphs)}")
for idx, p in enumerate(cell.paragraphs):
    print(f"  P[{idx}]: {p.text[:60]}")

