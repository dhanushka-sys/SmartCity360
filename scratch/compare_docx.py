import docx

doc1 = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")
doc2 = docx.Document(r"other_files\SmartCity360_OODP_II_Final_Submission.docx")

print(f"v5.docx: paragraphs={len(doc1.paragraphs)}, tables={len(doc1.tables)}")
print(f"other_files docx: paragraphs={len(doc2.paragraphs)}, tables={len(doc2.tables)}")

