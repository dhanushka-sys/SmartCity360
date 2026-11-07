import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")
print("TABLE 19:")
for p in doc.tables[19].rows[0].cells[0].paragraphs:
    print(p.text)

print("\nTABLE 20:")
for p in doc.tables[20].rows[0].cells[0].paragraphs:
    print(p.text)

