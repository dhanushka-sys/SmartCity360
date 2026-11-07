import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc_path = r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx"
backup_path = r"docs\backup\SmartCity360_OODP_II_Final_Submission-v5.before_cleanup.docx"
shutil.copyfile(doc_path, backup_path)
print(f"Backed up to: {backup_path}")

doc = docx.Document(doc_path)

# 1. CLEAN THE 14 FIGURE TABLES
# Table Index -> Image File
fig_mapping = [
    (2, "slide_03_p4_decorator_uml.png"),
    (3, "slide_04_p5_decorator_pipeline.png"),
    (5, "slide_05_p6_composite_uml.png"),
    (6, "slide_06_p7_composite_tree.png"),
    (8, "slide_07_p8_chain_uml.png"),
    (9, "slide_08_p9_chain_flow.png"),
    (11, "slide_09_p10_flyweight_uml.png"),
    (12, "slide_10_p11_flyweight_memory.png"),
    (14, "slide_11_p12_interpreter_uml.png"),
    (15, "slide_12_p13_interpreter_ast.png"),
    (17, "slide_01_p2_arch.png"),
    (18, "slide_13_p14_use_case.png"),
    (19, "slide_14_p15_sequence.png"),
    (20, "slide_15_p16_database.png"),
]

for t_idx, img_name in fig_mapping:
    img_path = os.path.join(r"scratch\slide_images", img_name)
    table = doc.tables[t_idx]
    cell = table.rows[0].cells[0]
    
    # Completely clear cell
    cell.text = ""
    
    # Single paragraph containing ONLY the centered image
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    
    run = p.add_run()
    run.add_picture(img_path, width=Inches(6.2))
    print(f"Cleaned Figure Table {t_idx:2d} -> ONLY {img_name}")

# 2. CLEAN LISTING TABLES (4, 7, 10, 13, 16)
listing_tables = [4, 7, 10, 13, 16]
for t_idx in listing_tables:
    table = doc.tables[t_idx]
    cell = table.rows[0].cells[0]
    raw_text = cell.text
    
    # Split lines and filter out ASCII box & candidate guide
    lines = raw_text.split('\n')
    cleaned_lines = []
    in_box = False
    for line in lines:
        if '┌' in line or '>>>' in line:
            in_box = True
            continue
        if '└' in line:
            in_box = False
            continue
        if in_box:
            continue
        if '📌' in line or 'Candidate' in line:
            continue
        cleaned_lines.append(line.rstrip())
        
    # Rebuild cell text cleanly
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    
    for i, line in enumerate(cleaned_lines):
        line_clean = line.replace(" PLACEHOLDER", "").replace("PLACEHOLDER — ", "")
        if not line_clean.strip():
            continue
        r = p.add_run(line_clean + "\n")
        r.font.name = "Times New Roman"
        if i == 0:
            r.bold = True
            r.font.size = Pt(10.5)
            r.font.color.rgb = RGBColor(15, 41, 74)
        elif i == 1:
            r.bold = True
            r.font.size = Pt(10.0)
            r.font.color.rgb = RGBColor(30, 58, 138)
        elif line_clean.startswith("Target Source File:"):
            r.bold = True
            r.font.size = Pt(9.0)
            r.font.color.rgb = RGBColor(15, 23, 42)
        elif line_clean.startswith("•"):
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(51, 65, 85)
        else:
            r.font.size = Pt(9.0)
            r.font.color.rgb = RGBColor(71, 85, 105)
            
    print(f"Cleaned Listing Table {t_idx:2d}")

# 3. CLEAN APPENDIX A TABLES (24 to 49)
for t_idx in range(24, 50):
    table = doc.tables[t_idx]
    cell = table.rows[0].cells[0]
    raw_text = cell.text
    
    lines = raw_text.split('\n')
    cleaned_lines = []
    in_box = False
    for line in lines:
        if '┌' in line or '>>>' in line:
            in_box = True
            continue
        if '└' in line:
            in_box = False
            continue
        if in_box:
            continue
        if '📌' in line or 'Candidate' in line:
            continue
        cleaned_lines.append(line.rstrip())
        
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    
    for i, line in enumerate(cleaned_lines):
        line_clean = line.replace(" PLACEHOLDER", "").replace("PLACEHOLDER — ", "")
        if not line_clean.strip():
            continue
        r = p.add_run(line_clean + ("\n" if i < len(cleaned_lines)-1 else ""))
        r.font.name = "Times New Roman"
        if i == 0:
            r.bold = True
            r.font.size = Pt(10.0)
            r.font.color.rgb = RGBColor(15, 41, 74)
        elif line_clean.startswith("File Path:"):
            r.bold = True
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(30, 58, 138)
        else:
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(51, 65, 85)
            
print("Cleaned Appendix A Tables (24 to 49)")

# 4. CLEAN PARAGRAPHS 63 & 66
for p in doc.paragraphs:
    if "Each figure location provides a structured placeholder and technical specification" in p.text:
        p.text = (
            "This technical assessment report incorporates 14 dedicated architectural diagrams, "
            "UML class models, behavioral sequence workflows, and system enterprise designs mapped "
            "directly to the assessment rubric. Each architectural figure is embedded within its designated "
            "system specification section below:"
        )
        p.style.font.name = "Times New Roman"
        print("Updated Paragraph 63")
        
    if "In accordance with Part F.3 of the assessment specification, raw source code text has been removed and replaced with dedicated screenshot containers" in p.text:
        p.text = (
            "In accordance with Part F.3 of the assessment specification, production source code architecture is "
            "formally documented through dedicated pattern listings and the comprehensive source catalog in Appendix A. "
            "The complete, compilable production source code is packaged in the accompanying project repository archive:"
        )
        p.style.font.name = "Times New Roman"
        print("Updated Paragraph 66")

# Save document
doc.save(doc_path)
print(f"Successfully saved updated document to: {doc_path} ({os.path.getsize(doc_path)} bytes)")

# Synchronize other_files copy
shutil.copyfile(doc_path, r"other_files\SmartCity360_OODP_II_Final_Submission.docx")
print("Synchronized to other_files copy.")

