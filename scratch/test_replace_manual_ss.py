import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
import shutil
import win32com.client
from pypdf import PdfReader
import pymupdf

# Current document
doc_path = r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx"
doc = docx.Document(doc_path)

manual_uploads = [
    (24, r"C:/Users/Dhanushka Maduranga/.gemini/antigravity/brain/0731c486-f798-497e-b236-2bb7f941f183/.user_uploaded/media_1794001135240_f3886161.png", "StreamData.java", 4.8),
    (25, r"C:/Users/Dhanushka Maduranga/.gemini/antigravity/brain/0731c486-f798-497e-b236-2bb7f941f183/.user_uploaded/media_1794001084914_965f4c95.jpg", "EnergyStreamData.java", 4.2),
    (26, r"C:/Users/Dhanushka Maduranga/.gemini/antigravity/brain/0731c486-f798-497e-b236-2bb7f941f183/.user_uploaded/media_1794001171394_3bb3dbaa.jpg", "StreamDataDecorator.java", 4.2),
]

for tbl_idx, img_src, name, width_in in manual_uploads:
    tbl = doc.tables[tbl_idx]
    cell = tbl.cell(0, 0)
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(img_src, width=Inches(width_in))
    print(f"Replaced Table {tbl_idx} ({name}) with width {width_in} in")

test_doc = r"scratch/test_manual_ss.docx"
doc.save(test_doc)

# Convert to PDF
word = win36_word = win32com.client.DispatchEx('Word.Application')
word.Visible = False
test_pdf = r"scratch/test_manual_ss.pdf"
try:
    wdoc = word.Documents.Open(os.path.abspath(test_doc))
    wdoc.SaveAs2(os.path.abspath(test_pdf), FileFormat=17)
    wdoc.Close(False)
finally:
    word.Quit()

reader = PdfReader(test_pdf)
print(f"Total page count: {len(reader.pages)}")

# Render pages around Appendix A
pdf_doc = pymupdf.open(test_pdf)
for p_no in range(44, len(pdf_doc)):
    page = pdf_doc[p_no]
    pix = page.get_pixmap(dpi=150)
    pix.save(f"scratch/test_manual_ss_page_{p_no+1}.png")
    print(f"Rendered Page {p_no+1}")

