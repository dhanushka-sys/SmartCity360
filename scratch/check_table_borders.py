import docx

doc = docx.Document(r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx")

for idx in [2, 4, 7, 10, 13, 16, 24]:
    t = doc.tables[idx]
    tblPr = t._element.tblPr
    print(f"Table {idx} tblPr:")
    print(tblPr.xml)

