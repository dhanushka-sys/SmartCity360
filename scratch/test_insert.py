import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import shutil

src = r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx"
dst = r"scratch\test_doc.docx"
shutil.copyfile(src, dst)

doc = docx.Document(dst)
table = doc.tables[2]
cell = table.rows[0].cells[0]

# Let's inspect paragraphs in cell
print(f"Original cell text length: {len(cell.text)}")

# We can replace cell contents
# Clear existing text
cell.text = "" # Clears all paragraphs except one empty paragraph

# First paragraph: Header & specs
p_head = cell.paragraphs[0]
p_head.paragraph_format.space_before = Pt(4)
p_head.paragraph_format.space_after = Pt(6)
p_head.paragraph_format.line_spacing = 1.15

r0 = p_head.add_run("📷 [ FIGURE 2.1 — ARCHITECTURAL DIAGRAM ]\n")
r0.bold = True
r0.font.name = "Arial"
r0.font.size = Pt(11)
r0.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

r1 = p_head.add_run("UML Class Diagram — Dynamic Security Decorator Pattern Architecture\n")
r1.bold = True
r1.font.name = "Arial"
r1.font.size = Pt(10)
r1.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

r2 = p_head.add_run("Diagram Category: UML Structural Class Diagram   •   Assessment Mapping: Part A.2 — Mechanism of Flexible & Layered Enhancement\n")
r2.italic = True
r2.font.name = "Arial"
r2.font.size = Pt(8.5)
r2.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)

specs = (
    "Key Architectural Elements & Specifications Included:\n"
    "• Component Interface: StreamData (getData(): String, getPayloadBytes(): byte[], getPayloadSize(): int, getDescription(): String)\n"
    "• Concrete Component: EnergyStreamData (implements StreamData, wraps raw telemetry JSON payload)\n"
    "• Abstract Decorator: StreamDataDecorator (implements StreamData, contains protected wrappee: StreamData, delegation constructor)\n"
    "• Concrete Decorators: EncryptionDecorator (AES-256-GCM AEAD encryption), CompressionDecorator (GZIP stream compaction), AuthenticationDecorator (HMAC-SHA256 authentication tag generator)\n"
    "• UML Relationships: Realization of StreamData, Aggregation (1 StreamDataDecorator wraps 1 StreamData), Generalization (concrete decorators extend StreamDataDecorator)"
)
r3 = p_head.add_run(specs)
r3.font.name = "Arial"
r3.font.size = Pt(8.5)
r3.font.color.rgb = RGBColor(0x37, 0x41, 0x51)

# Second paragraph: The Picture!
p_pic = cell.add_paragraph()
p_pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_pic.paragraph_format.space_before = Pt(8)
p_pic.paragraph_format.space_after = Pt(4)
run_pic = p_pic.add_run()
img_path = r"scratch\slide_images\slide_03_p4_decorator_uml.png"
run_pic.add_picture(img_path, width=Inches(6.0))

# Third paragraph: Verification caption
p_cap = cell.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cap.paragraph_format.space_before = Pt(2)
p_cap.paragraph_format.space_after = Pt(4)
r_cap = p_cap.add_run("Figure 2.1 — SmartCity360 Architectural Presentation (Slide 3: Part A, Decorator UML Class Diagram)")
r_cap.font.name = "Arial"
r_cap.font.size = Pt(8)
r_cap.italic = True
r_cap.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)

doc.save(dst)
print(f"Successfully saved test doc, size: {dst}")

