import os
import shutil
import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image

updates = [
    {
        "table_idx": 24,
        "src": r"C:/Users/Dhanushka Maduranga/.gemini/antigravity/brain/0731c486-f798-497e-b236-2bb7f941f183/.user_uploaded/media_1794001135240_f3886161.png",
        "dest": r"screenshots/appendix/StreamData.java.png",
        "name": "StreamData.java"
    },
    {
        "table_idx": 25,
        "src": r"C:/Users/Dhanushka Maduranga/.gemini/antigravity/brain/0731c486-f798-497e-b236-2bb7f941f183/.user_uploaded/media_1794001084914_965f4c95.jpg",
        "dest": r"screenshots/appendix/EnergyStreamData.java.png",
        "name": "EnergyStreamData.java"
    },
    {
        "table_idx": 26,
        "src": r"C:/Users/Dhanushka Maduranga/.gemini/antigravity/brain/0731c486-f798-497e-b236-2bb7f941f183/.user_uploaded/media_1794001171394_3bb3dbaa.jpg",
        "dest": r"screenshots/appendix/StreamDataDecorator.java.png",
        "name": "StreamDataDecorator.java"
    }
]

doc_path = r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx"
doc = docx.Document(doc_path)

for u in updates:
    # 1. Save / convert image
    im = Image.open(u["src"])
    im.save(u["dest"])
    print(f"Saved {u['dest']}, size: {im.size}")

    # 2. Update docx table
    tbl = doc.tables[u["table_idx"]]
    cell = tbl.cell(0, 0)
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(u["dest"], width=Inches(6.0))
    print(f"Updated Table {u['table_idx']} with {u['dest']}")

doc.save(doc_path)
print(f"Successfully saved {doc_path}")

other_path = r"other_files/SmartCity360_OODP_II_Final_Submission.docx"
shutil.copy2(doc_path, other_path)
print(f"Synced to {other_path}")

