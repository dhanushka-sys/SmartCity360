import os
import sys
import subprocess
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="CBD5E1", right="CBD5E1", sz="4"):
    tcPr = cell._tc.get_or_add_tcPr()
    top_xml = f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{top}"/>' if top != "none" else '<w:top w:val="none"/>'
    bottom_xml = f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{bottom}"/>' if bottom != "none" else '<w:bottom w:val="none"/>'
    left_xml = f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{left}"/>' if left != "none" else '<w:left w:val="none"/>'
    right_xml = f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{right}"/>' if right != "none" else '<w:right w:val="none"/>'
    
    borders_elm = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  {top_xml}\n'
        f'  {bottom_xml}\n'
        f'  {left_xml}\n'
        f'  {right_xml}\n'
        f'</w:tcBorders>'
    )
    tcPr.append(borders_elm)

def create_docx(filename):
    doc = Document()
    
    # Standard academic page setup - A4 with 1 inch (25.4 mm) margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        
        # Header - Formal Academic
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Java Institute for Advanced Technology — Unit: JIAT/OODP II | Assessment: EX/01")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(100, 116, 139)
        
        # Footer - Formal Academic
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("SmartCity360 Technical Report — Department of Examinations | Final Submission")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(100, 116, 139)

    # Base Styles: Times New Roman, 11.5pt, 1.25 line spacing
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(11.5)
    style_normal.font.color.rgb = RGBColor(30, 41, 59)
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(6)

    # ------------------ DOCUMENT TITLE HEADER ------------------
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(2)
    r_meta = p_meta.add_run(f"{content.METADATA['institution']} • Unit: {content.METADATA['unit_name']} ({content.METADATA['unit_id']}) • {content.METADATA['assessment_id']}")
    r_meta.font.name = "Times New Roman"
    r_meta.font.size = Pt(9)
    r_meta.font.color.rgb = RGBColor(30, 58, 138)
    r_meta.bold = True

    h_title = doc.add_heading(level=1)
    r_t = h_title.add_run("SMARTCITY360 MANAGEMENT PLATFORM")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(18)
    r_t.font.color.rgb = RGBColor(15, 41, 74)
    r_t.bold = True
    h_title.paragraph_format.space_after = Pt(2)

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Technical Design Pattern Implementation & Comprehensive Architectural Assessment Report")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11)
    r_sub.italic = True
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(30, 58, 138)
    p_sub.paragraph_format.space_after = Pt(4)

    p_info = doc.add_paragraph()
    r_inf = p_info.add_run(f"Industrial Context: {content.METADATA['company']} • Target City: {content.METADATA['target_city']} • Weighting: {content.METADATA['total_marks']}")
    r_inf.font.name = "Times New Roman"
    r_inf.font.size = Pt(9)
    r_inf.font.color.rgb = RGBColor(100, 116, 139)
    p_info.paragraph_format.space_after = Pt(14)
    # ------------------ TABLE OF CONTENTS ------------------
    h_toc = doc.add_heading(level=1)
    r_toc = h_toc.add_run("TABLE OF CONTENTS")
    r_toc.font.name = "Times New Roman"
    r_toc.font.size = Pt(14)
    r_toc.font.color.rgb = RGBColor(15, 41, 74)
    h_toc.paragraph_format.space_after = Pt(12)

    toc_items = [
        ("1. Executive Summary & Scenario Overview", "2"),
        ("2. Part A — Dynamic Security Wrappers for Data Streams (Decorator Pattern) [15 Marks]", "3"),
        ("    2.1 Identification & Architectural Justification (3 Marks)", "3"),
        ("    2.2 Mechanism of Flexible & Layered Enhancement (4 Marks)", "4"),
        ("    2.3 Long-Term Evaluation: Reusability, Extensibility & Anti-Pattern Mitigation (8 Marks)", "4"),
        ("    2.4 Object Wrapping Pipeline Flowchart & Technical Source Code Highlights", "5"),
        ("3. Part B — Hierarchical Structure of Smart Zones (Composite Pattern) [15 Marks]", "7"),
        ("    3.1 Identification & Architectural Justification (3 Marks)", "7"),
        ("    3.2 UML Class Diagram & Mechanism of the Hierarchical Composition (4 Marks)", "7"),
        ("    3.3 Evaluation: Scalability & Growing Infrastructure Management (8 Marks)", "8"),
        ("    3.4 UML Class Diagram & Technical Source Code Highlights", "9"),
        ("4. Part C — Escalation of Citizen Complaints (Chain of Responsibility Pattern) [15 Marks]", "11"),
        ("    4.1 Identification & Architectural Justification (3 Marks)", "11"),
        ("    4.2 Mechanism of Decoupled Request Handling (4 Marks)", "11"),
        ("    4.3 Evaluation of Flexibility, Traceability, Benefits & Trade-offs (8 Marks)", "12"),
        ("    4.4 Multi-Tier Escalation Flowchart & Technical Source Code Highlights", "12"),
        ("5. Part D — Efficient Management of Smart Street Lights (Flyweight Pattern) [15 Marks]", "14"),
        ("    5.1 Identification & Architectural Justification (3 Marks)", "14"),
        ("    5.2 Handling Shared Intrinsic vs Unique Extrinsic State (4 Marks)", "14"),
        ("    5.3 Quantitative Memory & Performance Impact Analysis (94.9% Reduction) (8 Marks)", "14"),
        ("    5.4 JVM Memory Pool Architecture Diagram & Technical Source Code Highlights", "16"),
        ("6. Part E — Interpreting City Policies Defined in DSL (Interpreter Pattern) [15 Marks]", "17"),
        ("    6.1 Identification & Architectural Justification (3 Marks)", "17"),
        ("    6.2 UML Class Diagram & Mechanism of the DSL Interpreter Pattern (4 Marks)", "17"),
        ("    6.3 Critical Assessment: Rule Updates, Extensibility & Security (8 Marks)", "18"),
        ("    6.4 UML Class Diagram & Technical Source Code Highlights", "18"),
        ("7. Part F — Final Project Demonstration, VIVA Defense & Video Outline [25 Marks]", "20"),
        ("    7.1 Overall System Architecture & Multi-Tier Enterprise Design", "20"),
        ("    7.2 Key Architectural Choices & Anti-Pattern Defense Matrix", "20"),
        ("    7.3 VIVA Oral Examination Questions & Comprehensive Model Answers (15 Marks)", "21"),
        ("    7.4 10–15 Minute Demonstration Video Walkthrough Script (10 Marks)", "22"),
        ("    7.5 Final Submission Deliverables Verification", "23"),
        ("8. Conclusion & Academic References", "25")
    ]
    for item, page in toc_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_after = Pt(2)
        r_txt = p_item.add_run(item)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(10.5)
        if item.startswith(" ") is False and not item.startswith("    "):
            r_txt.bold = True
            r_txt.font.color.rgb = RGBColor(15, 23, 42)
        else:
            r_txt.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_page_break()

    # ------------------ 1. EXECUTIVE SUMMARY ------------------
    h1 = doc.add_heading(level=1)
    r1 = h1.add_run("1. EXECUTIVE SUMMARY & SCENARIO OVERVIEW")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(14)
    r1.font.color.rgb = RGBColor(15, 41, 74)
    h1.paragraph_format.space_after = Pt(10)

    for para in content.EXEC_SUMMARY.split("\n\n"):
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run(para)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11.5)

    # ------------------ PARTS A - E ------------------
    def render_part(part_data, part_num, part_letter, figure_name):
        doc.add_page_break()
        h_part = doc.add_heading(level=1)
        r_part = h_part.add_run(f"{part_num}. {part_data['title']} [{part_data['marks']}]")
        r_part.font.name = "Times New Roman"
        r_part.font.size = Pt(14)
        r_part.font.color.rgb = RGBColor(15, 41, 74)
        h_part.paragraph_format.space_after = Pt(8)

        # Scenario
        p_scen = doc.add_paragraph()
        p_scen.paragraph_format.left_indent = Inches(0.2)
        p_scen.paragraph_format.right_indent = Inches(0.2)
        p_scen.paragraph_format.space_after = Pt(10)
        r_scen_title = p_scen.add_run("Scenario Description: ")
        r_scen_title.bold = True
        r_scen_title.font.name = "Times New Roman"
        r_scen_title.font.size = Pt(11)
        r_scen_title.font.color.rgb = RGBColor(30, 58, 138)
        r_scen_txt = p_scen.add_run(part_data["scenario"])
        r_scen_txt.font.italic = True
        r_scen_txt.font.name = "Times New Roman"
        r_scen_txt.font.size = Pt(11)
        r_scen_txt.font.color.rgb = RGBColor(51, 65, 85)

        # Questions
        for q_idx, q_key in enumerate(["q1", "q2", "q3"], 1):
            q_info = part_data[q_key]
            h_q = doc.add_heading(level=2)
            r_q = h_q.add_run(f"{part_num}.{q_idx} {q_info['title']}")
            r_q.font.name = "Times New Roman"
            r_q.font.size = Pt(12)
            r_q.bold = True
            r_q.font.color.rgb = RGBColor(30, 58, 138)
            h_q.paragraph_format.space_after = Pt(6)

            if "pattern" in q_info:
                p_pat = doc.add_paragraph()
                r_plbl = p_pat.add_run("Selected Design Pattern: ")
                r_plbl.bold = True
                r_plbl.font.name = "Times New Roman"
                r_plbl.font.size = Pt(11)
                r_plbl.font.color.rgb = RGBColor(15, 41, 74)
                r_pval = p_pat.add_run(q_info["pattern"])
                r_pval.bold = True
                r_pval.font.name = "Times New Roman"
                r_pval.font.size = Pt(11)
                r_pval.font.color.rgb = RGBColor(30, 58, 138)
                p_pat.paragraph_format.space_after = Pt(6)

            for paragraph_txt in q_info["content"].split("\n\n"):
                p_body = doc.add_paragraph()
                p_body.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p_body.paragraph_format.space_after = Pt(6)
                for line in paragraph_txt.split("\n"):
                    if line.strip().startswith("•") or line.strip().startswith("-") or line.strip().startswith("Step"):
                        r_line = p_body.add_run(line + "\n")
                        r_line.font.name = "Times New Roman"
                        r_line.font.size = Pt(11)
                    elif ":" in line and not line.strip().startswith("http"):
                        parts = line.split(":", 1)
                        r_h = p_body.add_run(parts[0] + ":")
                        r_h.bold = True
                        r_h.font.name = "Times New Roman"
                        r_h.font.size = Pt(11)
                        r_b = p_body.add_run(parts[1] + "\n")
                        r_b.font.name = "Times New Roman"
                        r_b.font.size = Pt(11)
                    else:
                        r_line = p_body.add_run(line + "\n")
                        r_line.font.name = "Times New Roman"
                        r_line.font.size = Pt(11)

        # Diagram Reference Box in Word
        p_diag = doc.add_paragraph()
        p_diag.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_diag.paragraph_format.space_after = Pt(10)
        r_df = p_diag.add_run(f"[{figure_name}]\n(Rendered as vector graphic in the companion academic PDF)")
        r_df.font.italic = True
        r_df.font.size = Pt(10)
        r_df.font.color.rgb = RGBColor(71, 85, 105)

        # Source Code Highlight Section
        h_code = doc.add_heading(level=2)
        r_code_t = h_code.add_run(f"{part_num}.4 Architectural Implementation Highlights (Zero Comments)")
        r_code_t.font.name = "Times New Roman"
        r_code_t.font.size = Pt(12)
        r_code_t.bold = True
        r_code_t.font.color.rgb = RGBColor(30, 58, 138)
        h_code.paragraph_format.space_after = Pt(6)

        p_code_note = doc.add_paragraph()
        r_cn = p_code_note.add_run("Key architectural implementation snippet demonstrating pattern structure (the complete compilable source codebase is packaged in the project archive):")
        r_cn.font.name = "Times New Roman"
        r_cn.font.size = Pt(10)
        r_cn.font.italic = True
        r_cn.font.color.rgb = RGBColor(100, 116, 139)
        p_code_note.paragraph_format.space_after = Pt(6)

        if "illustrative_code" in part_data and part_data["illustrative_code"]:
            tbl_c = doc.add_table(rows=1, cols=1)
            tbl_c.alignment = WD_TABLE_ALIGNMENT.CENTER
            c_cell = tbl_c.rows[0].cells[0]
            c_cell.width = Inches(6.5)
            set_cell_background(c_cell, "F8FAFC")
            set_cell_margins(c_cell, 60, 60, 80, 80)
            set_cell_borders(c_cell, top="CBD5E1", bottom="CBD5E1", left="1E3A8A", right="CBD5E1", sz="12")
            
            p_code = c_cell.paragraphs[0]
            p_code.paragraph_format.line_spacing = 1.0
            p_code.paragraph_format.space_after = Pt(0)
            r_code = p_code.add_run(part_data["illustrative_code"])
            r_code.font.name = "Consolas"
            r_code.font.size = Pt(8.5)
            r_code.font.color.rgb = RGBColor(15, 23, 42)

            p_sp = doc.add_paragraph()
            p_sp.paragraph_format.space_after = Pt(6)

    # Render Parts A-E
    render_part(content.PART_A, "2", "A", "Figure 2.1 — Dynamic Security Decorator Pipeline Flowchart")
    render_part(content.PART_B, "3", "B", "Figure 3.1 — Hierarchical Urban Zone Tree Topography Diagram")
    render_part(content.PART_C, "4", "C", "Figure 4.1 — Multi-Tier Citizen Grievance Escalation Flowchart")
    render_part(content.PART_D, "5", "D", "Figure 5.1 — JVM Heap Memory Allocation & Flyweight Pool Architecture")
    render_part(content.PART_E, "6", "E", "Figure 6.1 — Abstract Syntax Tree (AST) & Boolean Evaluation Flowchart")

    # ------------------ PART F ------------------
    doc.add_page_break()
    h_f = doc.add_heading(level=1)
    r_f = h_f.add_run("7. PART F — FINAL PROJECT DEMONSTRATION, VIVA DEFENSE & DOCUMENTATION [25 MARKS]")
    r_f.font.name = "Times New Roman"
    r_f.font.size = Pt(14)
    r_f.font.color.rgb = RGBColor(15, 41, 74)
    h_f.paragraph_format.space_after = Pt(10)

    # F.1
    h_f1 = doc.add_heading(level=2)
    r_f1 = h_f1.add_run("7.1 Overall System Architecture & Multi-Tier Enterprise Design")
    r_f1.font.name = "Times New Roman"
    r_f1.font.size = Pt(12)
    r_f1.bold = True
    r_f1.font.color.rgb = RGBColor(30, 58, 138)
    h_f1.paragraph_format.space_after = Pt(6)

    for p_txt in content.PART_F["f1_arch"].split("\n\n"):
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(p_txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    p_diag_f = doc.add_paragraph()
    p_diag_f.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_diag_f.paragraph_format.space_after = Pt(10)
    r_df2 = p_diag_f.add_run("[Figure 7.1 — End-to-End Enterprise Multi-Tier Platform Architecture Diagram]\n(Rendered as vector graphic in the companion academic PDF)")
    r_df2.font.italic = True
    r_df2.font.size = Pt(10)
    r_df2.font.color.rgb = RGBColor(71, 85, 105)

    # F.2
    h_f2 = doc.add_heading(level=2)
    r_f2 = h_f2.add_run("7.2 Key Architectural Choices & Anti-Pattern Defense Matrix")
    r_f2.font.name = "Times New Roman"
    r_f2.font.size = Pt(12)
    r_f2.bold = True
    r_f2.font.color.rgb = RGBColor(30, 58, 138)
    h_f2.paragraph_format.space_after = Pt(6)

    p_apd = doc.add_paragraph()
    r_ad = p_apd.add_run("The SmartCity360 platform actively mitigates all 8 foundational software anti-patterns identified in the curriculum:")
    r_ad.font.name = "Times New Roman"
    r_ad.font.size = Pt(11)

    # Formal table for anti-patterns
    tbl_ap = doc.add_table(rows=len(content.PART_F["f2_antipatterns"]) + 1, cols=3)
    tbl_ap.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tbl_ap.rows[0]
    for ci, htxt in enumerate(["Anti-Pattern", "Architectural Hazard & Symptom", "SmartCity360 Pattern Mitigation"]):
        cell = hdr.cells[ci]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(htxt)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    hdr.cells[0].width = Inches(1.5)
    hdr.cells[1].width = Inches(2.3)
    hdr.cells[2].width = Inches(2.7)

    for ri, (ap_name, ap_sym, ap_mit) in enumerate(content.PART_F["f2_antipatterns"]):
        row = tbl_ap.rows[ri + 1]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.width, c1.width, c2.width = Inches(1.5), Inches(2.3), Inches(2.7)
        bg = "F8FAFC" if ri % 2 == 0 else "FFFFFF"

        for ci, (cell, val) in enumerate([(c0, ap_name), (c1, ap_sym), (c2, ap_mit)]):
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 70, 70)
            set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="CBD5E1", right="CBD5E1")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(15, 23, 42)
            if ci == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 58, 138)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_after = Pt(12)

    # F.3 VIVA Q&A
    h_f3 = doc.add_heading(level=2)
    r_f3 = h_f3.add_run("7.3 VIVA Oral Examination Questions & Comprehensive Model Answers (15 Marks)")
    r_f3.font.name = "Times New Roman"
    r_f3.font.size = Pt(12)
    r_f3.bold = True
    r_f3.font.color.rgb = RGBColor(30, 58, 138)
    h_f3.paragraph_format.space_after = Pt(6)

    for idx, v_item in enumerate(content.PART_F["f3_viva"]):
        h_vq = doc.add_heading(level=3)
        r_vq = h_vq.add_run(f"Question {idx + 1}: \"{v_item['q']}\"")
        r_vq.font.name = "Times New Roman"
        r_vq.font.size = Pt(11)
        r_vq.bold = True
        r_vq.font.color.rgb = RGBColor(15, 41, 74)
        h_vq.paragraph_format.space_after = Pt(3)

        p_va = doc.add_paragraph()
        p_va.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_va.paragraph_format.left_indent = Inches(0.2)
        p_va.paragraph_format.space_after = Pt(8)
        r_lbl = p_va.add_run("Model Answer: ")
        r_lbl.bold = True
        r_lbl.font.name = "Times New Roman"
        r_lbl.font.size = Pt(10.5)
        r_lbl.font.color.rgb = RGBColor(30, 58, 138)
        r_txt = p_va.add_run(v_item["a"])
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = RGBColor(51, 65, 85)

    # F.4 Video Script
    h_f4 = doc.add_heading(level=2)
    r_f4 = h_f4.add_run("7.4 10–15 Minute Demonstration Video Walkthrough Script (10 Marks)")
    r_f4.font.name = "Times New Roman"
    r_f4.font.size = Pt(12)
    r_f4.bold = True
    r_f4.font.color.rgb = RGBColor(30, 58, 138)
    h_f4.paragraph_format.space_after = Pt(6)

    tbl_v = doc.add_table(rows=len(content.PART_F["f4_video_script"]) + 1, cols=3)
    tbl_v.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_v = tbl_v.rows[0]
    for ci, htxt in enumerate(["Timeframe", "Demonstration Phase", "Screen Action & Technical Narration"]):
        cell = hdr_v.cells[ci]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(htxt)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    hdr_v.cells[0].width = Inches(1.3)
    hdr_v.cells[1].width = Inches(2.2)
    hdr_v.cells[2].width = Inches(3.0)

    for ri, (v_time, v_phase, v_desc) in enumerate(content.PART_F["f4_video_script"]):
        row = tbl_v.rows[ri + 1]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.width, c1.width, c2.width = Inches(1.3), Inches(2.2), Inches(3.0)
        bg = "F8FAFC" if ri % 2 == 0 else "FFFFFF"

        for ci, (cell, val) in enumerate([(c0, v_time), (c1, v_phase), (c2, v_desc)]):
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 70, 70)
            set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="CBD5E1", right="CBD5E1")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(15, 23, 42)
            if ci == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 58, 138)
            elif ci == 1:
                r.bold = True

    p_sp3 = doc.add_paragraph()
    p_sp3.paragraph_format.space_after = Pt(16)

    # F.5 Deliverables Table
    h_f5 = doc.add_heading(level=2)
    r_f5 = h_f5.add_run("7.5 Final Submission Deliverables Verification")
    r_f5.font.name = "Times New Roman"
    r_f5.font.size = Pt(12)
    r_f5.bold = True
    r_f5.font.color.rgb = RGBColor(30, 58, 138)
    h_f5.paragraph_format.space_after = Pt(6)

    p_f5 = doc.add_paragraph()
    r_f5_p = p_f5.add_run("In accordance with Section 5 of the assessment specification (Part F), the three mandatory deliverables have been prepared, audited, and formatted for direct submission to the Java Institute Student Portal:")
    r_f5_p.font.name = "Times New Roman"
    r_f5_p.font.size = Pt(11)

    tbl_del = doc.add_table(rows=len(content.PART_F.get("f5_deliverables", [])) + 1, cols=4)
    tbl_del.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_del = tbl_del.rows[0]
    for ci, htxt in enumerate(["Requirement", "Portal Section", "Artifact File", "Verification Scope"]):
        cell = hdr_del.cells[ci]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(htxt)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    hdr_del.cells[0].width = Inches(1.5)
    hdr_del.cells[1].width = Inches(1.5)
    hdr_del.cells[2].width = Inches(1.8)
    hdr_del.cells[3].width = Inches(1.7)

    for ri, (req, portal, fmt, fn, desc) in enumerate(content.PART_F.get("f5_deliverables", [])):
        row = tbl_del.rows[ri + 1]
        c0, c1, c2, c3 = row.cells[0], row.cells[1], row.cells[2], row.cells[3]
        c0.width, c1.width, c2.width, c3.width = Inches(1.5), Inches(1.5), Inches(1.8), Inches(1.7)
        bg = "F8FAFC" if ri % 2 == 0 else "FFFFFF"

        for ci, (cell, val) in enumerate([(c0, req), (c1, f"{portal}\n({fmt})"), (c2, fn), (c3, desc)]):
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 70, 70)
            set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="CBD5E1", right="CBD5E1")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(15, 23, 42)
            if ci == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 58, 138)
            elif ci == 2:
                r.bold = True

    p_sp4 = doc.add_paragraph()
    p_sp4.paragraph_format.space_after = Pt(16)

    # ------------------ REFERENCES ------------------
    doc.add_page_break()
    h_ref = doc.add_heading(level=1)
    r_ref = h_ref.add_run("8. CONCLUSION & ACADEMIC REFERENCES")
    r_ref.font.name = "Times New Roman"
    r_ref.font.size = Pt(14)
    r_ref.font.color.rgb = RGBColor(15, 41, 74)
    h_ref.paragraph_format.space_after = Pt(10)

    p_conc = doc.add_paragraph()
    p_conc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_cc = p_conc.add_run("Conclusion:\n")
    r_cc.bold = True
    r_cc.font.name = "Times New Roman"
    r_cc.font.size = Pt(11.5)
    r_cctx = p_conc.add_run(
        "The SmartCity360 platform exemplifies how classic Gang of Four design patterns solve real-world, high-concurrency challenges in smart municipal infrastructure. By strategically combining structural (Decorator, Composite, Flyweight) and behavioral (Chain of Responsibility, Interpreter) patterns, the system achieves maximum extensibility, robust security, minimal resource consumption, and decoupled maintenance."
    )
    r_cctx.font.name = "Times New Roman"
    r_cctx.font.size = Pt(11.5)
    p_conc.paragraph_format.space_after = Pt(16)

    p_rlbl = doc.add_paragraph()
    r_rl = p_rlbl.add_run("Academic References & Literature:")
    r_rl.bold = True
    r_rl.font.name = "Times New Roman"
    r_rl.font.size = Pt(11.5)
    r_rl.font.color.rgb = RGBColor(15, 41, 74)
    p_rlbl.paragraph_format.space_after = Pt(6)

    for ref in content.REFERENCES:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.left_indent = Inches(0.3)
        p_r.paragraph_format.space_after = Pt(4)
        r = p_r.add_run("• " + ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(51, 65, 85)

    doc.save(filename)
    print(f"Successfully generated Formal DOCX: {filename}")

if __name__ == "__main__":
    out_docx = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SmartCity360_OODP_II_Final_Submission.docx")
    create_docx(out_docx)
