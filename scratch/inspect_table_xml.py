import docx
from docx.oxml import OxmlElement

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")
table = doc.tables[2]
print("Table XML preview:")
print(table._tbl.xml[:500])

