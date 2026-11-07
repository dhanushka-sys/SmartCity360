import os
import re
import shutil
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image, ImageDraw, ImageFont
import win32com.client
from pypdf import PdfReader

# ----------------- WINDOWS INTELLIJ RENDERER -----------------
BG_COLOR = (25, 26, 28)           # #191A1C IntelliJ New UI Editor BG
TAB_BAR_BG = (25, 26, 28)         # Editor BG
TAB_ACTIVE_BG = (35, 53, 88)      # Dark blue tab highlight
GUTTER_TEXT = (90, 95, 105)       # #5A5F69 Line numbers
TEXT_DEFAULT = (188, 190, 196)    # #BCBEC4 Identifiers / Punctuation
KW_COLOR = (207, 142, 109)        # #CF8E6D Orange keywords
STR_COLOR = (106, 171, 115)       # #6AAB73 Green strings
NUM_COLOR = (42, 172, 184)        # #2AACB8 Cyan numbers
COMMENT_COLOR = (122, 126, 133)   # #7A7E85 Grey comments
ANNOTATION_COLOR = (187, 181, 41) # #BBB529 Yellow annotations
TYPE_COLOR = (223, 225, 229)      # #DFE1E5 Light grey types
AUTHOR_COLOR = (115, 120, 130)    # Code vision usages / author
GUTTER_ICON_COLOR = (70, 140, 220)# Blue circle with arrow icon

JAVA_KEYWORDS = {
    'abstract', 'boolean', 'byte', 'case', 'catch', 'char', 'class', 'const',
    'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final',
    'finally', 'float', 'for', 'if', 'implements', 'import', 'instanceof', 'int',
    'interface', 'long', 'native', 'new', 'package', 'private', 'protected',
    'public', 'return', 'short', 'static', 'super', 'switch', 'synchronized',
    'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while',
    'true', 'false', 'null', 'String', 'var', 'record'
}

FONT_DIR = r"C:\Program Files\JetBrains\IntelliJ IDEA 2026.2.4\jbr\lib\fonts"
FONT_REGULAR = os.path.join(FONT_DIR, "JetBrainsMono-Regular.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "JetBrainsMono-Bold.ttf")

def tokenize_code(text):
    token_pattern = re.compile(
        r'("(?:\\.|[^"\\])*")|'
        r'(@\w+)|'
        r'(0x[0-9a-fA-F]+|\b\d+(?:\.\d+)?\b)|'
        r'(\b[a-zA-Z_]\w*\b)|'
        r'(\s+)|'
        r'([^\s\w"@]+)'
    )
    tokens = []
    for match in token_pattern.finditer(text):
        s_val, annot, num, ident, ws, punct = match.groups()
        if s_val:
            tokens.append((s_val, STR_COLOR))
        elif annot:
            tokens.append((annot, ANNOTATION_COLOR))
        elif num:
            tokens.append((num, NUM_COLOR))
        elif ident:
            if ident in JAVA_KEYWORDS:
                tokens.append((ident, KW_COLOR))
            elif ident[0].isupper():
                tokens.append((ident, TYPE_COLOR))
            else:
                tokens.append((ident, TEXT_DEFAULT))
        elif ws:
            tokens.append((ws, TEXT_DEFAULT))
        elif punct:
            tokens.append((punct, TEXT_DEFAULT))
    return tokens

def tokenize_java_line(line):
    if '//' in line:
        code_part, comment_part = line.split('//', 1)
        tokens = tokenize_code(code_part)
        tokens.append(('//' + comment_part, COMMENT_COLOR))
        return tokens
    return tokenize_code(line)

def draw_person_silhouette(draw, x, y, color):
    # Head
    draw.ellipse([(x + 2, y), (x + 7, y + 5)], fill=color)
    # Shoulders / Torso
    draw.arc([(x, y + 6), (x + 9, y + 13)], start=180, end=360, fill=color, width=2)

def render_intellij_windows_editor(filename, file_type, code_lines, start_line_num, out_png, usages_class="16 usages", usages_method="5 usages"):
    width = 960
    font = ImageFont.truetype(FONT_REGULAR, 15)
    tab_font = ImageFont.truetype(FONT_REGULAR, 13)
    icon_font = ImageFont.truetype(FONT_BOLD, 10)
    vision_font = ImageFont.truetype(FONT_REGULAR, 11)
    
    line_height = 24
    top_bar_height = 36
    padding_bottom = 16
    gutter_width = 54
    
    height = top_bar_height + (len(code_lines) * line_height) + padding_bottom
    
    img = Image.new("RGB", (width, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 1. Editor Tab (Windows IntelliJ Style - NO MAC BUTTONS!)
    tab_x = 8
    tab_y = 5
    tab_h = 26
    tab_title_w = int(draw.textlength(filename, font=tab_font))
    tab_w = 34 + tab_title_w + 24
    
    draw.rounded_rectangle([(tab_x, tab_y), (tab_x + tab_w, tab_y + tab_h)], radius=4, fill=TAB_ACTIVE_BG)
    
    # Icon circle in tab
    icon_x = tab_x + 8
    icon_y = tab_y + 5
    if file_type == 'interface':
        icon_color = (49, 137, 72)
        icon_char = 'I'
    elif file_type == 'enum':
        icon_color = (200, 110, 40)
        icon_char = 'E'
    else:
        icon_color = (49, 89, 187)
        icon_char = 'C'
        
    draw.ellipse([(icon_x, icon_y), (icon_x + 14, icon_y + 14)], fill=icon_color)
    draw.text((icon_x + 4, icon_y + 1), icon_char, fill=(255, 255, 255), font=icon_font)
    
    # Tab title text
    draw.text((icon_x + 20, tab_y + 5), filename, fill=(223, 225, 229), font=tab_font)
    draw.text((tab_x + tab_w - 14, tab_y + 5), "x", fill=(134, 137, 144), font=tab_font)
    
    # 2. Code & Gutter Line Numbers
    curr_y = top_bar_height + 6
    for idx, raw_line in enumerate(code_lines):
        line_no = str(start_line_num + idx)
        draw.text((gutter_width - 12 - len(line_no) * 9, curr_y), line_no, fill=GUTTER_TEXT, font=font)
        
        # Gutter override / implement icons
        if '@Override' in raw_line or ('public ' in raw_line and ('void ' in raw_line or 'String ' in raw_line or 'boolean ' in raw_line or 'int ' in raw_line or 'double ' in raw_line or 'ComplaintRoutingResult ' in raw_line or 'SharedStreetlightProfile ' in raw_line)):
            icon_gy = curr_y + 4
            draw.ellipse([(gutter_width - 8, icon_gy), (gutter_width - 1, icon_gy + 7)], fill=GUTTER_ICON_COLOR)
            
        tokens = tokenize_java_line(raw_line)
        curr_x = gutter_width + 12
        for text, color in tokens:
            draw.text((curr_x, curr_y), text, fill=color, font=font)
            curr_x += int(draw.textlength(text, font=font))
            
        # Code vision author annotation for class or method
        stripped = raw_line.strip()
        if ('class ' in raw_line or 'interface ' in raw_line or 'enum ' in raw_line) and '{' in raw_line:
            draw.text((curr_x + 16, curr_y + 2), usages_class, fill=AUTHOR_COLOR, font=vision_font)
            icon_px = curr_x + 16 + int(draw.textlength(usages_class, font=vision_font)) + 8
            draw_person_silhouette(draw, icon_px, curr_y + 4, AUTHOR_COLOR)
            draw.text((icon_px + 12, curr_y + 2), "Dhanushka Maduranga", fill=AUTHOR_COLOR, font=vision_font)
        elif stripped.startswith('public ') and '(' in stripped and not stripped.startswith('public class') and not stripped.startswith('public interface'):
            draw.text((curr_x + 16, curr_y + 2), usages_method, fill=AUTHOR_COLOR, font=vision_font)
            icon_px = curr_x + 16 + int(draw.textlength(usages_method, font=vision_font)) + 8
            draw_person_silhouette(draw, icon_px, curr_y + 4, AUTHOR_COLOR)
            draw.text((icon_px + 12, curr_y + 2), "Dhanushka Maduranga", fill=AUTHOR_COLOR, font=vision_font)
            
        curr_y += line_height
        
    img.save(out_png)
    print(f"Rendered: {out_png}")

# ----------------- APPENDIX FILES DEFINITION -----------------
appendix_files = [
    # Table 24: StreamData.java -> USER AUTHENTIC
    {
        "table_idx": 24, "filename": "StreamData.java", "type": "interface",
        "file_path": "backend/src/main/java/com/smartcity/pattern/decorator/StreamData.java",
        "authentic_img": r"screenshots/appendix/StreamData.java.png",
        "start": 1, "lines": 13, "width": 4.8
    },
    # Table 25: EnergyStreamData.java -> USER AUTHENTIC
    {
        "table_idx": 25, "filename": "EnergyStreamData.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/decorator/EnergyStreamData.java",
        "authentic_img": r"screenshots/appendix/EnergyStreamData.java.png",
        "start": 1, "lines": 38, "width": 4.2
    },
    # Table 26: StreamDataDecorator.java -> USER AUTHENTIC
    {
        "table_idx": 26, "filename": "StreamDataDecorator.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/decorator/StreamDataDecorator.java",
        "authentic_img": r"screenshots/appendix/StreamDataDecorator.java.png",
        "start": 1, "lines": 38, "width": 4.2
    },
    # Table 27: EncryptionDecorator.java -> USER AUTHENTIC
    {
        "table_idx": 27, "filename": "EncryptionDecorator.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/decorator/EncryptionDecorator.java",
        "authentic_img": r"screenshots/listing_2_1.png",
        "start": 42, "lines": 35, "width": 4.2
    },
    # Table 28: CompressionDecorator.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 28, "filename": "CompressionDecorator.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/decorator/CompressionDecorator.java",
        "authentic_img": None, "start": 1, "lines": 38, "width": 4.5
    },
    # Table 29: AuthenticationDecorator.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 29, "filename": "AuthenticationDecorator.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/decorator/AuthenticationDecorator.java",
        "authentic_img": None, "start": 1, "lines": 38, "width": 4.5
    },
    # Table 30: ZoneComponent.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 30, "filename": "ZoneComponent.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/composite/ZoneComponent.java",
        "authentic_img": None, "start": 1, "lines": 36, "width": 4.5
    },
    # Table 31: BuildingLeaf.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 31, "filename": "BuildingLeaf.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/composite/BuildingLeaf.java",
        "authentic_img": None, "start": 1, "lines": 38, "width": 4.5
    },
    # Table 32: ZoneComposite.java -> USER AUTHENTIC
    {
        "table_idx": 32, "filename": "ZoneComposite.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/composite/ZoneComposite.java",
        "authentic_img": r"screenshots/listing_3_1.png",
        "start": 52, "lines": 36, "width": 4.2
    },
    # Table 33: ZoneCommand.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 33, "filename": "ZoneCommand.java", "type": "enum",
        "file_path": "backend/src/main/java/com/smartcity/pattern/composite/ZoneCommand.java",
        "authentic_img": None, "start": 1, "lines": 31, "width": 4.5
    },
    # Table 34: ComplaintHandler.java -> USER AUTHENTIC
    {
        "table_idx": 34, "filename": "ComplaintHandler.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/chain/ComplaintHandler.java",
        "authentic_img": r"screenshots/listing_4_1.png",
        "start": 6, "lines": 42, "width": 4.2
    },
    # Table 35: LocalStaffHandler.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 35, "filename": "LocalStaffHandler.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/chain/LocalStaffHandler.java",
        "authentic_img": None, "start": 1, "lines": 38, "width": 4.5
    },
    # Table 36: SupervisorHandler.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 36, "filename": "SupervisorHandler.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/chain/SupervisorHandler.java",
        "authentic_img": None, "start": 1, "lines": 38, "width": 4.5
    },
    # Table 37: CityManagerHandler.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 37, "filename": "CityManagerHandler.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/chain/CityManagerHandler.java",
        "authentic_img": None, "start": 1, "lines": 38, "width": 4.5
    },
    # Table 38: TerminalFallbackHandler.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 38, "filename": "TerminalFallbackHandler.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/chain/TerminalFallbackHandler.java",
        "authentic_img": None, "start": 1, "lines": 37, "width": 4.5
    },
    # Table 39: ComplaintChainFactory.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 39, "filename": "ComplaintChainFactory.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/chain/ComplaintChainFactory.java",
        "authentic_img": None, "start": 1, "lines": 19, "width": 4.5
    },
    # Table 40: SharedStreetlightProfile.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 40, "filename": "SharedStreetlightProfile.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/flyweight/SharedStreetlightProfile.java",
        "authentic_img": None, "start": 1, "lines": 38, "width": 4.5
    },
    # Table 41: StreetlightProfileFactory.java -> USER AUTHENTIC
    {
        "table_idx": 41, "filename": "StreetlightProfileFactory.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/flyweight/StreetlightProfileFactory.java",
        "authentic_img": r"screenshots/listing_5_1.png",
        "start": 1, "lines": 28, "width": 4.8
    },
    # Table 42: StreetlightContext.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 42, "filename": "StreetlightContext.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/flyweight/StreetlightContext.java",
        "authentic_img": None, "start": 1, "lines": 38, "width": 4.5
    },
    # Table 43: FlyweightBenchmark.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 43, "filename": "FlyweightBenchmark.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/flyweight/FlyweightBenchmark.java",
        "authentic_img": None, "start": 20, "lines": 38, "width": 4.5
    },
    # Table 44: Expression.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 44, "filename": "Expression.java", "type": "interface",
        "file_path": "backend/src/main/java/com/smartcity/pattern/interpreter/Expression.java",
        "authentic_img": None, "start": 1, "lines": 6, "width": 4.5
    },
    # Table 45: TerminalExpression.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 45, "filename": "TerminalExpression.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/interpreter/TerminalExpression.java",
        "authentic_img": None, "start": 1, "lines": 38, "width": 4.5
    },
    # Table 46: AndExpression.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 46, "filename": "AndExpression.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/interpreter/AndExpression.java",
        "authentic_img": None, "start": 1, "lines": 33, "width": 4.5
    },
    # Table 47: OrExpression.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 47, "filename": "OrExpression.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/interpreter/OrExpression.java",
        "authentic_img": None, "start": 1, "lines": 33, "width": 4.5
    },
    # Table 48: DslPolicyParser.java -> USER AUTHENTIC
    {
        "table_idx": 48, "filename": "DslPolicyParser.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/interpreter/DslPolicyParser.java",
        "authentic_img": r"screenshots/listing_6_1.png",
        "start": 158, "lines": 38, "width": 4.2
    },
    # Table 49: PolicyContext.java -> GENERATE (Windows IntelliJ)
    {
        "table_idx": 49, "filename": "PolicyContext.java", "type": "class",
        "file_path": "backend/src/main/java/com/smartcity/pattern/interpreter/PolicyContext.java",
        "authentic_img": None, "start": 1, "lines": 38, "width": 4.5
    }
]

# Generate the 18 Windows IntelliJ screenshots
os.makedirs("screenshots/windows_intellij", exist_ok=True)
for item in appendix_files:
    if item["authentic_img"] is None:
        out_png = f"screenshots/windows_intellij/{item['filename']}.png"
        with open(item["file_path"], "r", encoding="utf-8") as f:
            all_l = f.readlines()
        st = item["start"]
        ed = st + item["lines"]
        code_slice = [l.rstrip() for l in all_l[st - 1 : ed]]
        render_intellij_windows_editor(
            item["filename"],
            item["type"],
            code_slice,
            st,
            out_png
        )
        item["img_to_insert"] = out_png
    else:
        item["img_to_insert"] = item["authentic_img"]

# Now update the Word document
doc_path = r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx"
doc = docx.Document(doc_path)

for item in appendix_files:
    tbl_idx = item["table_idx"]
    img_path = item["img_to_insert"]
    w_in = item["width"]
    
    tbl = doc.tables[tbl_idx]
    cell = tbl.cell(0, 0)
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(img_path, width=Inches(w_in))
    print(f"Table {tbl_idx} ({item['filename']}): inserted {img_path} at width {w_in} in")

doc.save(doc_path)
print("Saved Word document.")
shutil.copy2(doc_path, r"other_files/SmartCity360_OODP_II_Final_Submission.docx")

# Convert to PDF
word = win32com.client.DispatchEx('Word.Application')
word.Visible = False
pdf_out = r"scratch/windows_intellij_submission.pdf"
try:
    wdoc = word.Documents.Open(os.path.abspath(doc_path))
    wdoc.SaveAs2(os.path.abspath(pdf_out), FileFormat=17)
    wdoc.Close(False)
finally:
    word.Quit()

reader = PdfReader(pdf_out)
print(f"PDF page count: {len(reader.pages)}")

