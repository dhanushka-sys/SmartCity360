import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")
table = doc.tables[2]
print("Table tblPr XML:")
print(table._tbl.tblPr.xml)

