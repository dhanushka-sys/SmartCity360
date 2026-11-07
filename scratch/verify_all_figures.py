import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

fig_tables = [
    (2, "Figure 2.1", "Decorator UML Class Diagram"),
    (3, "Figure 2.2", "Decorator Pipeline Flowchart"),
    (5, "Figure 3.1", "Composite UML Class Diagram"),
    (6, "Figure 3.2", "Composite Zone Tree Hierarchy"),
    (8, "Figure 4.1", "Chain of Responsibility UML Class Diagram"),
    (9, "Figure 4.2", "Complaint Escalation Routing Flow"),
    (11, "Figure 5.1", "Flyweight UML Class Diagram"),
    (12, "Figure 5.2", "Flyweight Memory Impact Analysis"),
    (14, "Figure 6.1", "Interpreter UML Class Diagram"),
    (15, "Figure 6.2", "Interpreter AST Decomposition Flowchart"),
    (17, "Figure 7.1", "Multi-Tier System Architecture (Four Decoupled Tiers)"),
    (18, "Figure 7.2", "Comprehensive System Use Case Diagram"),
    (19, "Figure 7.3", "Complaint Submission Sequence & Component Interaction"),
    (20, "Figure 7.4", "Relational Database Entity-Relationship Diagram (MySQL 8)"),
]

print("=== VERIFYING EMBEDDED SLIDES IN DOCX ===")
all_ok = True
for t_idx, fig_id, expected_title in fig_tables:
    table = doc.tables[t_idx]
    cell = table.rows[0].cells[0]
    
    # Check image
    has_image = False
    for p in cell.paragraphs:
        for r in p.runs:
            if r._r.xpath('.//a:blip'):
                has_image = True
                break
                
    header = cell.paragraphs[0].text.split('\n')[0]
    sub = cell.paragraphs[0].text.split('\n')[1] if len(cell.paragraphs[0].text.split('\n')) > 1 else ""
    caption = cell.paragraphs[-1].text if len(cell.paragraphs) > 1 else ""
    
    status = "OK" if has_image else "FAIL"
    if not has_image:
        all_ok = False
    print(f"[{status}] Table {t_idx:2d} | {fig_id}: {expected_title}")
    print(f"       Header:  {header}")
    print(f"       Caption: {caption}")

print(f"\nAll 14 figures verified successfully: {all_ok}")

