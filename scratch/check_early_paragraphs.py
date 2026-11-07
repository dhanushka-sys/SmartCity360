import docx

doc = docx.Document(r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx")

for i in range(55):
    p = doc.paragraphs[i]
    if p.text.strip():
        print(f"P{i}: style='{p.style.name}': {p.text.strip()}")

