import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import shutil

src = r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx"
dst = r"scratch\test_clean_doc.docx"
shutil.copyfile(src, dst)

doc = docx.Document(dst)
table = doc.tables[2]
cell = table.rows[0].cells[0]

# Clear cell completely
cell.text = ""

# Add single paragraph for the image
p = cell.paragraphs[0]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(4)
p.paragraph_format.space_after = Pt(4)
run = p.add_run()
img_path = r"scratch\slide_images\slide_03_p4_decorator_uml.png"
run.add_picture(img_path, width=Inches(6.2))

doc.save(dst)
print("Saved test clean doc successfully!")

