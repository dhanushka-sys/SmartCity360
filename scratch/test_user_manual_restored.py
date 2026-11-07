import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
import shutil
import win32com.client
from pypdf import PdfReader
import pymupdf

doc_path = r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx"
doc = docx.Document(doc_path)

# Replace Tables 24, 25, 26 with user's manual screenshots
manual_appendix = [
    (24, r"screenshots/appendix/StreamData.java.png", "StreamData.java"),
    (25, r"screenshots/appendix/EnergyStreamData.java.png", "EnergyStreamData.java"),
    (26, r"screenshots/appendix/StreamDataDecorator.java.png", "StreamDataDecorator.java"),
]

for tbl_idx, img_path, name in manual_appendix:
    tbl = doc.tables[tbl_idx]
    cell = tbl.cell(0, 0)
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(img_path, width=Inches(6.0))
    print(f"Table {tbl_idx}: replaced with {name}")

test_docx = r"scratch/test_user_manual_restored.docx"
doc.save(test_docx)
print("Saved docx.")

# Convert to PDF
word = win32com.client.DispatchEx('Word.Application')
word.Visible = False
test_pdf = r"scratch/test_user_manual_restored.pdf"
try:
    wdoc = word.Documents.Open(os.path.abspath(test_docx))
    wdoc.SaveAs2(os.path.abspath(test_pdf), FileFormat=17)
    wdoc.Close(False)
finally:
    word.Quit()

reader = PdfReader(test_pdf)
print(f"Total pages: {len(reader.pages)}")

# Render pages around Appendix A
pdf_doc = pymupdf.open(test_pdf)
os.makedirs("scratch/user_manual_pages", exist_ok=True)
for p_no in range(44, len(pdf_doc)):
    page = pdf_doc[p_no]
    pix = page.get_pixmap(dpi=150)
    pix.save(f"scratch/user_manual_pages/page_{p_no+1}.png")
    print(f"Rendered Page {p_no+1}")

