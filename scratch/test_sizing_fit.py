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

# Sizing test:
# Table 24 (StreamData.java): width 4.8 in -> height 2.4 in
# Table 25 (EnergyStreamData.java): width 4.2 in -> height 3.5 in
# Table 26 (StreamDataDecorator.java): width 4.2 in -> height 4.3 in

sizing = [
    (24, r"screenshots/appendix/StreamData.java.png", 4.8),
    (25, r"screenshots/appendix/EnergyStreamData.java.png", 4.2),
    (26, r"screenshots/appendix/StreamDataDecorator.java.png", 4.2),
]

for tbl_idx, img_path, w_in in sizing:
    tbl = doc.tables[tbl_idx]
    cell = tbl.cell(0, 0)
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(img_path, width=Inches(w_in))

test_docx = r"scratch/test_fit_page.docx"
doc.save(test_docx)

word = win32com.client.DispatchEx('Word.Application')
word.Visible = False
test_pdf = r"scratch/test_fit_page.pdf"
try:
    wdoc = word.Documents.Open(os.path.abspath(test_docx))
    wdoc.SaveAs2(os.path.abspath(test_pdf), FileFormat=17)
    wdoc.Close(False)
finally:
    word.Quit()

reader = PdfReader(test_pdf)
print(f"Total pages with proportional sizing: {len(reader.pages)}")

pdf_doc = pymupdf.open(test_pdf)
for p_no in [44, 45, 46]:
    if p_no < len(pdf_doc):
        page = pdf_doc[p_no]
        pix = page.get_pixmap(dpi=150)
        pix.save(f"scratch/fit_page_{p_no+1}.png")
        print(f"Rendered fit_page_{p_no+1}")

