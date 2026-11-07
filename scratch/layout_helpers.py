import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image
import os
import io

def set_cell_margins_zero(cell):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m in ['top', 'bottom', 'left', 'right']:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), '0')
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def remove_table_borders(table):
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

def make_subtle_table_card(table, border_color="E5E7EB", bg_color="FAFAFA"):
    tblPr = table._element.tblPr
    tblBorders = tblPr.find(qn('w:tblBorders'))
    if tblBorders is not None:
        tblPr.remove(tblBorders)
    newBorders = OxmlElement('w:tblBorders')
    for b in ['top', 'bottom', 'left', 'right']:
        node = OxmlElement(f'w:{b}')
        node.set(qn('w:val'), 'single')
        node.set(qn('w:sz'), '4') # 0.5 pt subtle
        node.set(qn('w:space'), '0')
        node.set(qn('w:color'), border_color)
        newBorders.append(node)
    for b in ['insideH', 'insideV']:
        node = OxmlElement(f'w:{b}')
        node.set(qn('w:val'), 'none')
        newBorders.append(node)
    tblPr.append(newBorders)

print("Helper functions ready.")

