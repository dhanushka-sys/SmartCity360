import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

for i in range(8, 55):
    p = doc.paragraphs[i]
    if p.text.strip():
        print(f"P[{i}]: {repr(p.text.strip())}")

