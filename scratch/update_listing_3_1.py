import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import shutil
import os

src_img = r"C:/Users/Dhanushka Maduranga/.gemini/antigravity/brain/0731c486-f798-497e-b236-2bb7f941f183/.user_uploaded/media_1793987968153_185dc3dd.jpg"
dest_img = r"screenshots/listing_3_1.png"

# Convert/save to listing_3_1.png
im = Image.open(src_img)
im.save(dest_img)
print(f"Saved {dest_img}, size: {im.size}")

doc_path = r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx"
doc = docx.Document(doc_path)

# Verify Table 7
table = doc.tables[7]
cell = table.cell(0, 0)
print(f"Table 7 cell paragraphs before: {len(cell.paragraphs)}")
for i, p in enumerate(cell.paragraphs):
    print(f"P{i}: text='{p.text[:60]}', runs={len(p.runs)}")

# Clear cell text completely and add single centered image paragraph
cell.text = ""
p = cell.paragraphs[0]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run.add_picture(dest_img, width=Inches(6.0))

doc.save(doc_path)
print(f"Successfully updated {doc_path}")

# Sync to other_files
other_path = r"other_files/SmartCity360_OODP_II_Final_Submission.docx"
shutil.copy2(doc_path, other_path)
print(f"Synced to {other_path}")

