import os
import shutil
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc_path = r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx"
backup_path = r"docs\backup\SmartCity360_OODP_II_Final_Submission-v5.before_clean_listing_text.docx"
shutil.copyfile(doc_path, backup_path)
print(f"Backed up to: {backup_path}")

doc = docx.Document(doc_path)

listing_images = [
    (4, r"screenshots\listing_2_1.png"),
    (7, r"screenshots\listing_3_1.png"),
    (10, r"screenshots\listing_4_1.png"),
    (13, r"screenshots\listing_5_1.png"),
    (16, r"screenshots\listing_6_1.png"),
]

for t_idx, img_path in listing_images:
    table = doc.tables[t_idx]
    cell = table.rows[0].cells[0]
    
    # Completely clear all text paragraphs
    cell.text = ""
    
    # Single paragraph containing ONLY the centered picture
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    
    run = p.add_run()
    run.add_picture(img_path, width=Inches(6.2))
    print(f"Cleaned Table {t_idx:2d} -> ONLY {img_path}")

doc.save(doc_path)
print(f"Saved cleaned document to: {doc_path} ({os.path.getsize(doc_path)} bytes)")

# Synchronize other_files copy
shutil.copyfile(doc_path, r"other_files\SmartCity360_OODP_II_Final_Submission.docx")
print("Synchronized other_files copy.")

