import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

print("=== TABLE 4 text ===")
print(doc.tables[4].rows[0].cells[0].text)

print("\n=== TABLE 24 text ===")
print(doc.tables[24].rows[0].cells[0].text[:300])

