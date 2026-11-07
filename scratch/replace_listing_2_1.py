import os
import shutil
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image

uploaded_img = r"C:\Users\Dhanushka Maduranga\.gemini\antigravity\brain\0731c486-f798-497e-b236-2bb7f941f183\.user_uploaded\media_1793987511302_37593d67.jpg"
target_img = r"screenshots\listing_2_1.png"

# Save high quality PNG copy into screenshots folder
with Image.open(uploaded_img) as im:
    im.save(target_img, format="PNG")
print(f"Copied uploaded image to {target_img} ({os.path.getsize(target_img)} bytes)")

# Update docx
doc_path = r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx"
doc = docx.Document(doc_path)

table = doc.tables[4] # Listing 2.1
cell = table.rows[0].cells[0]
cell.text = ""

p = cell.paragraphs[0]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(4)
p.paragraph_format.space_after = Pt(4)
p.paragraph_format.line_spacing = 1.0

run = p.add_run()
run.add_picture(target_img, width=Inches(6.0))

doc.save(doc_path)
print(f"Updated Table 4 in {doc_path} with new IntelliJ screenshot!")

# Synchronize other_files copy
shutil.copyfile(doc_path, r"other_files\SmartCity360_OODP_II_Final_Submission.docx")
print("Synchronized other_files copy.")

