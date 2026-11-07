import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image
import io
import os
import shutil
import win32com.client
from pypdf import PdfReader

def clean_table_borders_and_margins(table):
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

    for row in table.rows:
        trPr = row._element.get_or_add_trPr()
        cantSplit = OxmlElement('w:cantSplit')
        trPr.append(cantSplit)
        for cell in row.cells:
            tcPr = cell._element.get_or_add_tcPr()
            shd = tcPr.find(qn('w:shd'))
            if shd is not None:
                tcPr.remove(shd)
            tcBorders = tcPr.find(qn('w:tcBorders'))
            if tcBorders is not None:
                tcPr.remove(tcBorders)
            tcMar = tcPr.find(qn('w:tcMar'))
            if tcMar is not None:
                tcMar.clear()
            else:
                tcMar = OxmlElement('w:tcMar')
                tcPr.append(tcMar)
            for m in ['top', 'bottom', 'left', 'right']:
                node = OxmlElement(f'w:{m}')
                node.set(qn('w:w'), '0')
                node.set(qn('w:type'), 'dxa')
                tcMar.append(node)

def add_pb(p):
    pPr = p._element.get_or_add_pPr()
    pb = OxmlElement('w:pageBreakBefore')
    pPr.append(pb)

def resize_drawing_in_cell(cell, target_w_in, target_h_in):
    cx = int(target_w_in * 914400)
    cy = int(target_h_in * 914400)
    for ext in cell._element.xpath('.//wp:extent'):
        ext.set('cx', str(cx))
        ext.set('cy', str(cy))
    for ae in cell._element.xpath('.//a:xfrm/a:ext'):
        ae.set('cx', str(cx))
        ae.set('cy', str(cy))

doc_path = r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx"
doc = docx.Document(doc_path)

# 1. Clear all pageBreakBefore
for p in doc.paragraphs:
    pPr = p._element.pPr
    if pPr is not None:
        pb = pPr.find(qn('w:pageBreakBefore'))
        if pb is not None:
            pPr.remove(pb)

# 2. Add pageBreakBefore only on exact major section heads
target_indices = [4, 68, 78, 150, 226, 284, 346, 389, 423, 435]
for idx in target_indices:
    if idx < len(doc.paragraphs):
        add_pb(doc.paragraphs[idx])
        print(f"Added pageBreakBefore to P{idx}: {doc.paragraphs[idx].text[:50]}")

# 3. Heading keep_with_next
for p in doc.paragraphs:
    t = p.text.strip()
    if p.style.name.startswith('Heading') or any(t.startswith(x) for x in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', 'Figure ', 'Listing ', 'Screenshot ']):
        p.paragraph_format.keep_with_next = True

# 4. Process Tables 2 to 20 (Body figures & listings)
for idx in range(2, 21):
    tbl = doc.tables[idx]
    clean_table_borders_and_margins(tbl)
    cell = tbl.cell(0, 0)
    p = cell.paragraphs[0]
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    is_listing = idx in [4, 7, 10, 13, 16]
    blips = cell._element.xpath('.//a:blip/@r:embed')
    if blips:
        part = doc.part.related_parts[blips[0]]
        im = Image.open(io.BytesIO(part.blob))
        w, h = im.size
        aspect = w / h
        if is_listing:
            # Code listing: max height 3.0 in, max width 4.5 in
            th = min(3.0, 4.5 / aspect)
            tw = th * aspect
        else:
            # Diagram: 16:9 -> 5.4 in wide, 3.03 in tall
            tw = min(5.4, 3.1 * aspect)
            th = tw / aspect
        resize_drawing_in_cell(cell, tw, th)

# 5. Process Appendix Tables 24 to 49
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
        part = doc.part.related_parts[blips[0]]
        im = Image.open(io.BytesIO(part.blob))
        w, h = im.size
        aspect = w / h
        # Target height: 2.3 in, max width 4.2 in
        th = min(2.3, 4.2 / aspect)
        tw = th * aspect
        resize_drawing_in_cell(cell, tw, th)

doc.save(doc_path)
print("Saved fixed document.")
shutil.copy2(doc_path, r"other_files/SmartCity360_OODP_II_Final_Submission.docx")

# Export to PDF via Word COM
pdf_path = r"scratch/fixed.pdf"
word = win32com.client.DispatchEx('Word.Application')
word.Visible = False
try:
    wdoc = word.Documents.Open(os.path.abspath(doc_path))
    wdoc.SaveAs2(os.path.abspath(pdf_path), FileFormat=17)
    wdoc.Close(False)
finally:
    word.Quit()

reader = PdfReader(pdf_path)
print(f"Fixed PDF total page count: {len(reader.pages)}")

