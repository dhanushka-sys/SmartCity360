import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")
print("TABLE 1:")
for r in doc.tables[1].rows:
    print([c.text.strip().replace('\n', ' ') for c in r.cells])

