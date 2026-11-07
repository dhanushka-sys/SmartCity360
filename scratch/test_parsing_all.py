import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

mapping = [
    (2, "Figure 2.1", "slide_03_p4_decorator_uml.png", "Slide 3: Part A, Decorator UML Class Diagram"),
    (3, "Figure 2.2", "slide_04_p5_decorator_pipeline.png", "Slide 4: Part A, Decorator Runtime Pipeline & Nesting"),
    (5, "Figure 3.1", "slide_05_p6_composite_uml.png", "Slide 5: Part B, Composite UML Class Diagram"),
    (6, "Figure 3.2", "slide_06_p7_composite_tree.png", "Slide 6: Part B, Composite Zone Tree & Command Broadcast"),
    (8, "Figure 4.1", "slide_07_p8_chain_uml.png", "Slide 7: Part C, Chain of Responsibility UML Class Diagram"),
    (9, "Figure 4.2", "slide_08_p9_chain_flow.png", "Slide 8: Part C, Chain of Responsibility Routing Flow"),
    (11, "Figure 5.1", "slide_09_p10_flyweight_uml.png", "Slide 9: Part D, Flyweight UML Class Diagram"),
    (12, "Figure 5.2", "slide_10_p11_flyweight_memory.png", "Slide 10: Part D, Flyweight Memory Impact at 25,000 Poles"),
    (14, "Figure 6.1", "slide_11_p12_interpreter_uml.png", "Slide 11: Part E, Interpreter UML Class Diagram"),
    (15, "Figure 6.2", "slide_12_p13_interpreter_ast.png", "Slide 12: Part E, Interpreter AST for Sample Policy"),
    (17, "Figure 7.1", "slide_01_p2_arch.png", "Slide 1: System Architecture - Four Decoupled Tiers"),
    (18, "Figure 7.2", "slide_13_p14_use_case.png", "Slide 13: System Design - Comprehensive Use Case Diagram"),
    (19, "Figure 7.3", "slide_14_p15_sequence.png", "Slide 14: System Design - Complaint Submission Sequence & Component Interaction"),
    (20, "Figure 7.4", "slide_15_p16_database.png", "Slide 15: System Design - Database Model (MySQL 8)"),
]

for t_idx, fig_id, img_name, slide_desc in mapping:
    table = doc.tables[t_idx]
    cell = table.rows[0].cells[0]
    full_text = cell.text
    
    # Split by ASCII box
    lines = full_text.split('\n')
    header_lines = []
    for line in lines:
        if '┌' in line or '>>>' in line:
            break
        header_lines.append(line.rstrip())
        
    print(f"\n[{fig_id}] Table {t_idx} -> {img_name}")
    print(f"  Header lines count: {len(header_lines)}")
    print(f"  Line 0: {header_lines[0] if header_lines else ''}")
    print(f"  Line 1: {header_lines[1] if len(header_lines) > 1 else ''}")
    print(f"  Line 2: {header_lines[2] if len(header_lines) > 2 else ''}")
    print(f"  Line 3: {header_lines[3] if len(header_lines) > 3 else ''}")
    print(f"  Total characters in header: {sum(len(l) for l in header_lines)}")

