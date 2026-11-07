import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
import shutil
import win32com.client
from pypdf import PdfReader

# Load before_clean_listing_text.docx which has the exact original design
source_backup = r"docs/backup/SmartCity360_OODP_II_Final_Submission-v5.before_clean_listing_text.docx"
doc = docx.Document(source_backup)

# Replace the 5 main listings with the user's authentic IntelliJ screenshots
listings_to_replace = [
    (4, r"screenshots/listing_2_1.png"),
    (7, r"screenshots/listing_3_1.png"),
    (10, r"screenshots/listing_4_1.png"),
    (13, r"screenshots/listing_5_1.png"),
    (16, r"screenshots/listing_6_1.png"),
]

for tbl_idx, img_path in listings_to_replace:
    tbl = doc.tables[tbl_idx]
    cell = tbl.cell(0, 0)
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(img_path, width=Inches(6.0))
    print(f"Table {tbl_idx}: replaced with {img_path}")

test_out = r"scratch/restored_old_design.docx"
doc.save(test_out)
print(f"Saved {test_out}")

# Convert to PDF to check
word = win32com.client.DispatchEx('Word.Application')
word.Visible = False
pdf_out = r"scratch/restored_old_design.pdf"
try:
    wdoc = word.Documents.Open(os.path.abspath(test_out))
    wdoc.SaveAs2(os.path.abspath(pdf_out), FileFormat=17)
    wdoc.Close(False)
finally:
    word.Quit()

reader = PdfReader(pdf_out)
print(f"Restored design PDF total page count: {len(reader.pages)}")

