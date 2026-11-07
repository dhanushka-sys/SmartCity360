import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 1. Backup original document
doc_path = r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx"
backup_path = r"docs\backup\SmartCity360_OODP_II_Final_Submission-v5.before_slides_insert.docx"
os.makedirs(os.path.dirname(backup_path), exist_ok=True)
shutil.copyfile(doc_path, backup_path)
print(f"Backed up original document to: {backup_path}")

doc = docx.Document(doc_path)

# Mapping of Table Index -> (Figure ID, Image Filename, Slide Title, Formal Caption)
mapping = [
    (2, "Figure 2.1", "slide_03_p4_decorator_uml.png", 
     "Slide 3: Part A, Decorator UML Class Diagram",
     "Figure 2.1: UML Class Diagram — Dynamic Security Decorator Pattern Architecture"),
     
    (3, "Figure 2.2", "slide_04_p5_decorator_pipeline.png", 
     "Slide 4: Part A, Decorator Runtime Pipeline & Nesting",
     "Figure 2.2: Data Stream Dynamic Wrapping Pipeline & Execution Flowchart"),
     
    (5, "Figure 3.1", "slide_05_p6_composite_uml.png", 
     "Slide 5: Part B, Composite UML Class Diagram",
     "Figure 3.1: UML Class Diagram — Hierarchical Smart Zones Composite Pattern"),
     
    (6, "Figure 3.2", "slide_06_p7_composite_tree.png", 
     "Slide 6: Part B, Composite Zone Tree & Command Broadcast",
     "Figure 3.2: Hierarchical Urban Zone Topography & Object Composition Hierarchy"),
     
    (8, "Figure 4.1", "slide_07_p8_chain_uml.png", 
     "Slide 7: Part C, Chain of Responsibility UML Class Diagram",
     "Figure 4.1: UML Class Diagram — Multi-Tier Complaint Escalation Chain of Responsibility"),
     
    (9, "Figure 4.2", "slide_08_p9_chain_flow.png", 
     "Slide 8: Part C, Chain of Responsibility Routing Flow",
     "Figure 4.2: Citizen Complaint Dynamic Escalation Workflow & Decision Flowchart"),
     
    (11, "Figure 5.1", "slide_09_p10_flyweight_uml.png", 
     "Slide 9: Part D, Flyweight UML Class Diagram",
     "Figure 5.1: UML Class Diagram — Smart Streetlight Flyweight Pattern Architecture"),
     
    (12, "Figure 5.2", "slide_10_p11_flyweight_memory.png", 
     "Slide 10: Part D, Flyweight Memory Impact at 25,000 Poles",
     "Figure 5.2: JVM Heap Memory Allocation: Flyweight Shared Pool vs Unoptimized Heap Graph"),
     
    (14, "Figure 6.1", "slide_11_p12_interpreter_uml.png", 
     "Slide 11: Part E, Interpreter UML Class Diagram",
     "Figure 6.1: UML Class Diagram — Municipal Policy DSL Grammar & Interpreter Pattern"),
     
    (15, "Figure 6.2", "slide_12_p13_interpreter_ast.png", 
     "Slide 12: Part E, Interpreter AST for Sample Policy",
     "Figure 6.2: Abstract Syntax Tree (AST) Decomposition & Boolean Evaluation Flowchart"),
     
    (17, "Figure 7.1", "slide_01_p2_arch.png", 
     "Slide 1: System Architecture - Four Decoupled Tiers",
     "Figure 7.1: End-to-End SmartCity360 Multi-Tier Enterprise Platform Architecture Diagram"),
     
    (18, "Figure 7.2", "slide_13_p14_use_case.png", 
     "Slide 13: System Design - Comprehensive Use Case Diagram",
     "Figure 7.2: SmartCity360 Comprehensive System Use Case Diagram"),
     
    (19, "Figure 7.3", "slide_14_p15_sequence.png", 
     "Slide 14: System Design - Complaint Submission Sequence & Subsystem Component Interaction",
     "Figure 7.3: Architectural Package Structure & Subsystem Component Interaction Diagram"),
     
    (20, "Figure 7.4", "slide_15_p16_database.png", 
     "Slide 15: System Design - Database Model (MySQL 8)",
     "Figure 7.4: SmartCity360 Relational Database Entity-Relationship Diagram (ERD)"),
]

for t_idx, fig_id, img_name, slide_title, formal_caption in mapping:
    img_path = os.path.join(r"scratch\slide_images", img_name)
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Missing image: {img_path}")
        
    table = doc.tables[t_idx]
    cell = table.rows[0].cells[0]
    raw_text = cell.text
    
    # Extract header lines before the ASCII box
    lines = raw_text.split('\n')
    header_lines = []
    for line in lines:
        if '┌' in line or '>>>' in line:
            break
        header_lines.append(line.rstrip())
        
    # Extract Title and Category
    title_line = ""
    cat_line = ""
    spec_lines = []
    
    # Usually:
    # Line 0: 📷 [ FIGURE PLACEHOLDER — FIGURE X.Y ]
    # Line 1: [Diagram Title]
    # Line 2: Diagram Category: ...
    # Line 3+: Key Architectural Elements...
    if len(header_lines) > 1:
        title_line = header_lines[1]
    if len(header_lines) > 2 and "Diagram Category:" in header_lines[2]:
        cat_line = header_lines[2]
        spec_lines = header_lines[3:]
    else:
        spec_lines = header_lines[2:]
        
    specs_text = "\n".join(spec_lines).strip()
    
    # Clear the cell
    cell.text = ""
    
    # Paragraph 0: Header & Specifications
    p_head = cell.paragraphs[0]
    p_head.paragraph_format.space_before = Pt(4)
    p_head.paragraph_format.space_after = Pt(4)
    p_head.paragraph_format.line_spacing = 1.15
    
    r0 = p_head.add_run(f"📷 [ {fig_id.upper()} — ARCHITECTURAL SPECIFICATION & DIAGRAM ARTIFACT ]\n")
    r0.bold = True
    r0.font.name = "Arial"
    r0.font.size = Pt(10.5)
    r0.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
    
    if title_line:
        r1 = p_head.add_run(f"{title_line}\n")
        r1.bold = True
        r1.font.name = "Arial"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
        
    if cat_line:
        r2 = p_head.add_run(f"{cat_line}\n")
        r2.italic = True
        r2.font.name = "Arial"
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)
        
    if specs_text:
        r3 = p_head.add_run(f"{specs_text}")
        r3.font.name = "Arial"
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = RGBColor(0x37, 0x41, 0x51)
        
    # Paragraph 1: High-Resolution Centered Image
    p_img = cell.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(4)
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(6.0))
    
    # Paragraph 2: Embedded Caption
    p_cap = cell.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(4)
    r_cap = p_cap.add_run(f"{fig_id} — SmartCity360 Architectural Presentation ({slide_title})")
    r_cap.italic = True
    r_cap.font.name = "Arial"
    r_cap.font.size = Pt(8.0)
    r_cap.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)
    
    print(f"Updated Table {t_idx} -> {fig_id} with {img_name} successfully.")

# Save updated docx
doc.save(doc_path)
print(f"Successfully saved updated document to: {doc_path} ({os.path.getsize(doc_path)} bytes)")

# Also update other_files copy if applicable
other_copy = r"other_files\SmartCity360_OODP_II_Final_Submission.docx"
try:
    shutil.copyfile(doc_path, other_copy)
    print(f"Synchronized copy to: {other_copy}")
except Exception as e:
    print(f"Could not update other_files copy: {e}")

