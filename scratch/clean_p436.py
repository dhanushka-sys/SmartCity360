import docx
import shutil

doc_path = r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx"
doc = docx.Document(doc_path)

p = doc.paragraphs[436]
p.text = (
    "This appendix provides a structured, formal catalog of all production source code files developed for the "
    "SmartCity360 municipal platform. In compliance with Part F.3 of the assessment specification ('prepare comprehensive "
    "project documentation, including working code to illustrate the design and functionality of your application'), "
    "each pattern's source files are mapped with their exact repository paths, architectural roles, and formal "
    "implementation references. The complete, compilable source files are packaged in the project repository and cataloged below:"
)
p.style.font.name = "Times New Roman"

doc.save(doc_path)
shutil.copyfile(doc_path, r"other_files\SmartCity360_OODP_II_Final_Submission.docx")
print("Updated Paragraph 436 successfully!")

