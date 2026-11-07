import os
import shutil
import io
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

def clean_table_borders_and_margins(table):
    # Set table borders to none
    tblPr = table._element.tblPr
    tblBorders = tblPr.find(qn('w:tblBorders'))
    if tblBorders is not None:
        tblPr.remove(tblBorders)
    newBorders = OxmlElement('w:tblBorders')
    for b in ['top', 'bottom', 'left', 'right', 'insideH', 'insideV']:
        node = OxmlElement(f'w:{b}')
        node.set(qn('w:val'), 'none')
        newBorders.append(node)
    tblPr.append(newBorders)

    # Set table cell margins to 0 and remove white background
    for row in table.rows:
        trPr = row._element.get_or_add_trPr()
        # cantSplit to avoid row breaking awkwardly
        cantSplit = OxmlElement('w:cantSplit')
        trPr.append(cantSplit)
        for cell in row.cells:
            tcPr = cell._element.get_or_add_tcPr()
            # clear shading
            shd = tcPr.find(qn('w:shd'))
            if shd is not None:
                tcPr.remove(shd)
            # clear tcBorders
            tcBorders = tcPr.find(qn('w:tcBorders'))
            if tcBorders is not None:
                tcPr.remove(tcBorders)
            # zero cell margins
            tcMar = tcPr.find(qn('w:tcMar'))
            if tcMar is not None:
                tcPr.remove(tcMar)
            newMar = OxmlElement('w:tcMar')
            for m in ['top', 'bottom', 'left', 'right']:
                node = OxmlElement(f'w:{m}')
                node.set(qn('w:w'), '0')
                node.set(qn('w:type'), 'dxa')
                newMar.append(node)
            tcPr.append(newMar)

def add_page_break_before_p(p):
    pPr = p._element.get_or_add_pPr()
    pageBreak = OxmlElement('w:pageBreakBefore')
    pPr.append(pageBreak)

def optimize_entire_document():
    doc_path = r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx"
    doc = docx.Document(doc_path)

    # 1. Page breaks on major sections
    major_headings = [
        "TABLE OF CONTENTS",
        "1. Executive Summary & Scenario Overview",
        "2. Part A — Dynamic Security Wrappers for Data Streams",
        "3. Part B — Hierarchical Structure of Smart Zones",
        "4. Part C — Escalation of Citizen Complaints",
        "5. Part D — Efficient Management of Smart Street Lights",
        "6. Part E — Interpreting City Policies Defined in DSL",
        "7. Part F — Final Project Demonstration, VIVA Defense & Video Outline",
        "8. Conclusion & Academic References",
        "9. APPENDIX A — COMPREHENSIVE SOURCE CODE IMPLEMENTATION SCREENSHOT CATALOG"
    ]

    for p in doc.paragraphs:
        p_text = p.text.strip()
        for mh in major_headings:
            if p_text.startswith(mh):
                add_page_break_before_p(p)
                p.paragraph_format.keep_with_next = True
                print(f"Added pageBreakBefore to: {mh}")
                break
        # Also keep headings with next paragraph
        if p.style.name.startswith('Heading') or any(p_text.startswith(x) for x in ['2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', 'Figure ', 'Listing ', 'Screenshot ']):
            p.paragraph_format.keep_with_next = True

    # 2. Main Body Figures & Listings (Tables 2 to 20)
    for idx in range(2, 21):
        tbl = doc.tables[idx]
        clean_table_borders_and_margins(tbl)
        cell = tbl.cell(0, 0)
        p = cell.paragraphs[0]
        p.paragraph_format.keep_with_next = True
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Find picture run
        # We resize pictures based on table type
        # Tables 4, 7, 10, 13, 16 are code listings (IntelliJ screenshots)
        # Tables 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 19, 20 are diagrams
        is_listing = idx in [4, 7, 10, 13, 16]

        # Extract image bytes from blip to get aspect ratio
        blips = cell._element.xpath('.//a:blip/@r:embed')
        if blips:
            rel_id = blips[0]
            part = doc.part.related_parts[rel_id]
            im = Image.open(io.BytesIO(part.blob))
            w, h = im.size
            aspect = w / h

            # Find cx, cy in inline/anchor
            extents = cell._element.xpath('.//wp:extent')
            if extents:
                ext = extents[0]
                if is_listing:
                    # Target max height = 3.2 inches, or max width = 4.8 inches
                    target_h_in = min(3.2, 4.8 / aspect)
                    target_w_in = target_h_in * aspect
                else:
                    # Diagram: width 5.4 inches, height ~3.0 inches
                    target_w_in = min(5.4, 3.2 * aspect)
                    target_h_in = target_w_in / aspect

                cx = int(target_w_in * 914400)
                cy = int(target_h_in * 914400)
                ext.set('cx', str(cx))
                ext.set('cy', str(cy))

                # Also update a:ext inside graphicData if present
                a_exts = cell._element.xpath('.//a:xfrm/a:ext')
                for ae in a_exts:
                    ae.set('cx', str(cx))
                    ae.set('cy', str(cy))

    # 3. Appendix A Screenshots (Tables 24 to 49)
    # Size them so exactly 2 fit per page: max height = 2.7 inches, max width = 4.8 inches
    for idx in range(24, 50):
        tbl = doc.tables[idx]
        clean_table_borders_and_margins(tbl)
        cell = tbl.cell(0, 0)
        p = cell.paragraphs[0]
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        blips = cell._element.xpath('.//a:blip/@r:embed')
        if blips:
            rel_id = blips[0]
            part = doc.part.related_parts[rel_id]
            im = Image.open(io.BytesIO(part.blob))
            w, h = im.size
            aspect = w / h

            extents = cell._element.xpath('.//wp:extent')
            if extents:
                ext = extents[0]
                # Target height = 2.6 inches, max width = 4.8 inches
                target_h_in = min(2.6, 4.8 / aspect)
                target_w_in = target_h_in * aspect

                cx = int(target_w_in * 914400)
                cy = int(target_h_in * 914400)
                ext.set('cx', str(cx))
                ext.set('cy', str(cy))

                a_exts = cell._element.xpath('.//a:xfrm/a:ext')
                for ae in a_exts:
                    ae.set('cx', str(cx))
                    ae.set('cy', str(cy))

    doc.save(doc_path)
    print("Successfully optimized document layout.")
    shutil.copy2(doc_path, r"other_files/SmartCity360_OODP_II_Final_Submission.docx")
    print("Synced to other_files.")

if __name__ == "__main__":
    optimize_entire_document()

