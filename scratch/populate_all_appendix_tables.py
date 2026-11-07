import os
import re
import shutil
import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image, ImageDraw, ImageFont

BG_COLOR = (30, 31, 34)       # #1E1F22 IntelliJ Dark
TAB_BAR_BG = (43, 45, 48)     # #2B2D30
TAB_ACTIVE_BG = (30, 31, 34)  # #1E1F22
BORDER_COLOR = (57, 59, 64)   # #393B40
GUTTER_LINE = (49, 52, 56)    # #313438
GUTTER_TEXT = (90, 95, 105)   # #5A5F69
TEXT_DEFAULT = (188, 190, 196)# #BCBEC4
KW_COLOR = (207, 142, 109)    # #CF8E6D orange
STR_COLOR = (106, 171, 115)   # #6AAB73 green
NUM_COLOR = (42, 172, 184)    # #2AACB8 cyan
COMMENT_COLOR = (122, 126, 133)# #7A7E85 grey
ANNOTATION_COLOR = (187, 181, 41) # #BBB529 yellow
TYPE_COLOR = (223, 225, 229)  # #DFE1E5 light grey
AUTHOR_COLOR = (120, 125, 135)# #787D87 code vision

JAVA_KEYWORDS = {
    'abstract', 'boolean', 'byte', 'case', 'catch', 'char', 'class', 'const',
    'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final',
    'finally', 'float', 'for', 'if', 'implements', 'import', 'instanceof', 'int',
    'interface', 'long', 'native', 'new', 'package', 'private', 'protected',
    'public', 'return', 'short', 'static', 'super', 'switch', 'synchronized',
    'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while',
    'true', 'false', 'null', 'String', 'var', 'record'
}

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

def render_code_window(filename, path_crumbs, code_lines, start_line_num, out_png):
    width = 1450
    font_path = r"C:\Windows\Fonts\consola.ttf"
    font = ImageFont.truetype(font_path, 20)
    title_font = ImageFont.truetype(font_path, 17)
    crumb_font = ImageFont.truetype(font_path, 14)
    vision_font = ImageFont.truetype(font_path, 13)
    
    line_height = 30
    top_bar_height = 40
    crumb_bar_height = 26
    header_height = top_bar_height + crumb_bar_height
    padding_bottom = 15
    
    height = header_height + (len(code_lines) * line_height) + padding_bottom
    gutter_width = 80
    
    img = Image.new("RGB", (width, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 1. Top Tab Bar
    draw.rectangle([(0, 0), (width, top_bar_height)], fill=TAB_BAR_BG)
    dot_y = top_bar_height // 2
    draw.ellipse([(16, dot_y - 6), (28, dot_y + 6)], fill=(237, 106, 94))
    draw.ellipse([(34, dot_y - 6), (46, dot_y + 6)], fill=(245, 191, 79))
    draw.ellipse([(52, dot_y - 6), (64, dot_y + 6)], fill=(98, 197, 84))
    
    # Active Tab
    tab_x = 85
    tab_w = max(260, int(draw.textlength(filename, font=title_font)) + 50)
    draw.rectangle([(tab_x, 5), (tab_x + tab_w, top_bar_height)], fill=TAB_ACTIVE_BG)
    draw.line([(tab_x, 5), (tab_x + tab_w, 5)], fill=(53, 116, 240), width=2)
    draw.text((tab_x + 14, 11), filename, fill=(223, 225, 229), font=title_font)
    draw.text((tab_x + tab_w - 22, 11), "x", fill=(134, 137, 144), font=title_font)
    
    # 2. Breadcrumbs Bar
    draw.rectangle([(0, top_bar_height), (width, header_height)], fill=(38, 40, 44))
    draw.text((16, top_bar_height + 5), path_crumbs, fill=(134, 137, 144), font=crumb_font)
    draw.line([(0, header_height), (width, header_height)], fill=BORDER_COLOR, width=1)
    
    # 3. Gutter Divider
    draw.line([(gutter_width, header_height), (gutter_width, height)], fill=GUTTER_LINE, width=1)
    
    # 4. Code & Line Numbers
    curr_y = header_height + 8
    first_class_found = False
    for idx, raw_line in enumerate(code_lines):
        line_no = str(start_line_num + idx)
        draw.text((gutter_width - 12 - len(line_no) * 11, curr_y), line_no, fill=GUTTER_TEXT, font=font)
        
        tokens = tokenize_java_line(raw_line)
        curr_x = gutter_width + 16
        for text, color in tokens:
            draw.text((curr_x, curr_y), text, fill=color, font=font)
            curr_x += int(draw.textlength(text, font=font))
            
        # Code vision author annotation for class or interface definition
        if ('class ' in raw_line or 'interface ' in raw_line or 'enum ' in raw_line) and not first_class_found:
            first_class_found = True
            draw.text((curr_x + 25, curr_y + 3), "Dhanushka Maduranga", fill=AUTHOR_COLOR, font=vision_font)
            
        curr_y += line_height
        
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline=BORDER_COLOR, width=1)
    img.save(out_png)
    print(f"Rendered: {out_png}")

# Appendix metadata
appendix_items = [
    {
        "table_idx": 24,
        "filename": "StreamData.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/decorator/StreamData.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > decorator > StreamData",
        "start_line": 1,
        "end_line": 12,
        "existing_img": None
    },
    {
        "table_idx": 25,
        "filename": "EnergyStreamData.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/decorator/EnergyStreamData.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > decorator > EnergyStreamData",
        "start_line": 1,
        "end_line": 37,
        "existing_img": None
    },
    {
        "table_idx": 26,
        "filename": "StreamDataDecorator.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/decorator/StreamDataDecorator.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > decorator > StreamDataDecorator",
        "start_line": 1,
        "end_line": 37,
        "existing_img": None
    },
    {
        "table_idx": 27,
        "filename": "EncryptionDecorator.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/decorator/EncryptionDecorator.java",
        "crumbs": "",
        "start_line": 1,
        "end_line": 40,
        "existing_img": r"screenshots/listing_2_1.png"
    },
    {
        "table_idx": 28,
        "filename": "CompressionDecorator.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/decorator/CompressionDecorator.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > decorator > CompressionDecorator",
        "start_line": 1,
        "end_line": 45,
        "existing_img": None
    },
    {
        "table_idx": 29,
        "filename": "AuthenticationDecorator.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/decorator/AuthenticationDecorator.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > decorator > AuthenticationDecorator",
        "start_line": 1,
        "end_line": 45,
        "existing_img": None
    },
    {
        "table_idx": 30,
        "filename": "ZoneComponent.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/composite/ZoneComponent.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > composite > ZoneComponent",
        "start_line": 1,
        "end_line": 45,
        "existing_img": None
    },
    {
        "table_idx": 31,
        "filename": "BuildingLeaf.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/composite/BuildingLeaf.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > composite > BuildingLeaf",
        "start_line": 1,
        "end_line": 45,
        "existing_img": None
    },
    {
        "table_idx": 32,
        "filename": "ZoneComposite.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/composite/ZoneComposite.java",
        "crumbs": "",
        "start_line": 1,
        "end_line": 45,
        "existing_img": r"screenshots/listing_3_1.png"
    },
    {
        "table_idx": 33,
        "filename": "ZoneCommand.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/composite/ZoneCommand.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > composite > ZoneCommand",
        "start_line": 1,
        "end_line": 31,
        "existing_img": None
    },
    {
        "table_idx": 34,
        "filename": "ComplaintHandler.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/chain/ComplaintHandler.java",
        "crumbs": "",
        "start_line": 1,
        "end_line": 45,
        "existing_img": r"screenshots/listing_4_1.png"
    },
    {
        "table_idx": 35,
        "filename": "LocalStaffHandler.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/chain/LocalStaffHandler.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > chain > LocalStaffHandler",
        "start_line": 1,
        "end_line": 44,
        "existing_img": None
    },
    {
        "table_idx": 36,
        "filename": "SupervisorHandler.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/chain/SupervisorHandler.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > chain > SupervisorHandler",
        "start_line": 1,
        "end_line": 44,
        "existing_img": None
    },
    {
        "table_idx": 37,
        "filename": "CityManagerHandler.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/chain/CityManagerHandler.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > chain > CityManagerHandler",
        "start_line": 1,
        "end_line": 40,
        "existing_img": None
    },
    {
        "table_idx": 38,
        "filename": "TerminalFallbackHandler.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/chain/TerminalFallbackHandler.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > chain > TerminalFallbackHandler",
        "start_line": 1,
        "end_line": 37,
        "existing_img": None
    },
    {
        "table_idx": 39,
        "filename": "ComplaintChainFactory.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/chain/ComplaintChainFactory.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > chain > ComplaintChainFactory",
        "start_line": 1,
        "end_line": 19,
        "existing_img": None
    },
    {
        "table_idx": 40,
        "filename": "SharedStreetlightProfile.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/flyweight/SharedStreetlightProfile.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > flyweight > SharedStreetlightProfile",
        "start_line": 1,
        "end_line": 45,
        "existing_img": None
    },
    {
        "table_idx": 41,
        "filename": "StreetlightProfileFactory.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/flyweight/StreetlightProfileFactory.java",
        "crumbs": "",
        "start_line": 1,
        "end_line": 45,
        "existing_img": r"screenshots/listing_5_1.png"
    },
    {
        "table_idx": 42,
        "filename": "StreetlightContext.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/flyweight/StreetlightContext.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > flyweight > StreetlightContext",
        "start_line": 1,
        "end_line": 45,
        "existing_img": None
    },
    {
        "table_idx": 43,
        "filename": "FlyweightBenchmark.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/flyweight/FlyweightBenchmark.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > flyweight > FlyweightBenchmark",
        "start_line": 20,
        "end_line": 65,
        "existing_img": None
    },
    {
        "table_idx": 44,
        "filename": "Expression.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/interpreter/Expression.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > interpreter > Expression",
        "start_line": 1,
        "end_line": 6,
        "existing_img": None
    },
    {
        "table_idx": 45,
        "filename": "TerminalExpression.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/interpreter/TerminalExpression.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > interpreter > TerminalExpression",
        "start_line": 1,
        "end_line": 45,
        "existing_img": None
    },
    {
        "table_idx": 46,
        "filename": "AndExpression.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/interpreter/AndExpression.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > interpreter > AndExpression",
        "start_line": 1,
        "end_line": 33,
        "existing_img": None
    },
    {
        "table_idx": 47,
        "filename": "OrExpression.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/interpreter/OrExpression.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > interpreter > OrExpression",
        "start_line": 1,
        "end_line": 33,
        "existing_img": None
    },
    {
        "table_idx": 48,
        "filename": "DslPolicyParser.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/interpreter/DslPolicyParser.java",
        "crumbs": "",
        "start_line": 1,
        "end_line": 45,
        "existing_img": r"screenshots/listing_6_1.png"
    },
    {
        "table_idx": 49,
        "filename": "PolicyContext.java",
        "file_path": "backend/src/main/java/com/smartcity/pattern/interpreter/PolicyContext.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > interpreter > PolicyContext",
        "start_line": 1,
        "end_line": 45,
        "existing_img": None
    }
]

print("=== STEP 1: RENDERING IMAGES ===")
os.makedirs("screenshots/appendix", exist_ok=True)
doc_path = r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx"
doc = docx.Document(doc_path)

for item in appendix_items:
    tbl_idx = item["table_idx"]
    fname = item["filename"]
    
    if item["existing_img"] and os.path.exists(item["existing_img"]):
        img_to_insert = item["existing_img"]
        print(f"Using existing authentic screenshot for Table {tbl_idx}: {img_to_insert}")
    else:
        out_img_path = f"screenshots/appendix/{fname}.png"
        real_code_path = item["file_path"]
        with open(real_code_path, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
        start_l = item["start_line"]
        end_l = min(len(all_lines), item["end_line"])
        slice_lines = [l.rstrip() for l in all_lines[start_l - 1 : end_l]]
        
        render_code_window(
            fname,
            item["crumbs"],
            slice_lines,
            start_l,
            out_img_path
        )
        img_to_insert = out_img_path
    
    # Insert into Word table
    tbl = doc.tables[tbl_idx]
    cell = tbl.cell(0, 0)
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(img_to_insert, width=Inches(6.0))
    print(f"Inserted into Table {tbl_idx}: {img_to_insert}")

doc.save(doc_path)
print(f"Saved {doc_path}")

other_path = r"other_files/SmartCity360_OODP_II_Final_Submission.docx"
shutil.copy2(doc_path, other_path)
print(f"Synced to {other_path}")

