import os
import re
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image, ImageDraw, ImageFont

os.makedirs("screenshots", exist_ok=True)

# ----------------- SYNTAX HIGHLIGHTER & RENDERER -----------------
BG_COLOR = (30, 31, 34)       # #1E1F22
TAB_BAR_BG = (43, 45, 48)     # #2B2D30
TAB_ACTIVE_BG = (30, 31, 34)  # #1E1F22
BORDER_COLOR = (57, 59, 64)   # #393B40
GUTTER_LINE = (49, 52, 56)    # #313438
GUTTER_TEXT = (90, 95, 105)   # #5A5F69
TEXT_DEFAULT = (188, 190, 196)# #BCBEC4
KW_COLOR = (207, 142, 109)    # #CF8E6D
STR_COLOR = (106, 171, 115)   # #6AAB73
NUM_COLOR = (42, 172, 184)    # #2AACB8
COMMENT_COLOR = (122, 126, 133)# #7A7E85
ANNOTATION_COLOR = (187, 181, 41) # #BBB529
METHOD_COLOR = (86, 168, 245) # #56A8F5
TYPE_COLOR = (223, 225, 229)  # #DFE1E5

JAVA_KEYWORDS = {
    'abstract', 'boolean', 'byte', 'case', 'catch', 'char', 'class', 'const',
    'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final',
    'finally', 'float', 'for', 'if', 'implements', 'import', 'instanceof', 'int',
    'interface', 'long', 'native', 'new', 'package', 'private', 'protected',
    'public', 'return', 'short', 'static', 'super', 'switch', 'synchronized',
    'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while',
    'true', 'false', 'null', 'String', 'var'
}

def tokenize_java_line(line):
    if '//' in line:
        code_part, comment_part = line.split('//', 1)
        tokens = tokenize_code(code_part)
        tokens.append(('//' + comment_part, COMMENT_COLOR))
        return tokens
    return tokenize_code(line)

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

def render_code_window(filename, path_crumbs, code_lines, start_line_num, out_png):
    width = 1500
    font_path = r"C:\Windows\Fonts\consola.ttf"
    font = ImageFont.truetype(font_path, 21)
    title_font = ImageFont.truetype(font_path, 18)
    crumb_font = ImageFont.truetype(font_path, 15)
    
    line_height = 32
    top_bar_height = 42
    crumb_bar_height = 28
    header_height = top_bar_height + crumb_bar_height
    padding_bottom = 20
    
    height = header_height + (len(code_lines) * line_height) + padding_bottom
    gutter_width = 85
    
    img = Image.new("RGB", (width, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 1. Top Tab Bar
    draw.rectangle([(0, 0), (width, top_bar_height)], fill=TAB_BAR_BG)
    dot_y = top_bar_height // 2
    draw.ellipse([(18, dot_y - 6), (30, dot_y + 6)], fill=(237, 106, 94))
    draw.ellipse([(38, dot_y - 6), (50, dot_y + 6)], fill=(245, 191, 79))
    draw.ellipse([(58, dot_y - 6), (70, dot_y + 6)], fill=(98, 197, 84))
    
    # Active Tab
    tab_x = 90
    tab_w = 280
    draw.rectangle([(tab_x, 6), (tab_x + tab_w, top_bar_height)], fill=TAB_ACTIVE_BG)
    draw.line([(tab_x, 6), (tab_x + tab_w, 6)], fill=(53, 116, 240), width=2)
    draw.text((tab_x + 16, 12), filename, fill=(223, 225, 229), font=title_font)
    draw.text((tab_x + tab_w - 24, 12), "×", fill=(134, 137, 144), font=title_font)
    
    # 2. Breadcrumbs Bar
    draw.rectangle([(0, top_bar_height), (width, header_height)], fill=(38, 40, 44))
    draw.text((20, top_bar_height + 5), path_crumbs, fill=(134, 137, 144), font=crumb_font)
    draw.line([(0, header_height), (width, header_height)], fill=BORDER_COLOR, width=1)
    
    # 3. Gutter Divider
    draw.line([(gutter_width, header_height), (gutter_width, height)], fill=GUTTER_LINE, width=1)
    
    # 4. Code & Line Numbers
    curr_y = header_height + 10
    for idx, raw_line in enumerate(code_lines):
        line_no = str(start_line_num + idx)
        draw.text((gutter_width - 15 - len(line_no) * 12, curr_y), line_no, fill=GUTTER_TEXT, font=font)
        
        tokens = tokenize_java_line(raw_line)
        curr_x = gutter_width + 20
        for text, color in tokens:
            draw.text((curr_x, curr_y), text, fill=color, font=font)
            curr_x += int(draw.textlength(text, font=font))
            
        curr_y += line_height
        
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline=BORDER_COLOR, width=1)
    img.save(out_png)
    print(f"Rendered: {out_png} ({width}x{height})")

# ----------------- GENERATE THE 5 PRIMARY LISTINGS -----------------
listings_meta = [
    {
        "table_idx": 4,
        "listing_id": "Listing 2.1",
        "file": "backend/src/main/java/com/smartcity/pattern/decorator/EncryptionDecorator.java",
        "tab_name": "EncryptionDecorator.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > decorator > EncryptionDecorator",
        "start_line": 43,
        "end_line": 73,
        "out_img": r"screenshots\listing_2_1.png"
    },
    {
        "table_idx": 7,
        "listing_id": "Listing 3.1",
        "file": "backend/src/main/java/com/smartcity/pattern/composite/ZoneComposite.java",
        "tab_name": "ZoneComposite.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > composite > ZoneComposite",
        "start_line": 52,
        "end_line": 88,
        "out_img": r"screenshots\listing_3_1.png"
    },
    {
        "table_idx": 10,
        "listing_id": "Listing 4.1",
        "file": "backend/src/main/java/com/smartcity/pattern/chain/ComplaintHandler.java",
        "tab_name": "ComplaintHandler.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > chain > ComplaintHandler",
        "start_line": 7,
        "end_line": 46,
        "out_img": r"screenshots\listing_4_1.png"
    },
    {
        "table_idx": 13,
        "listing_id": "Listing 5.1",
        "file": "backend/src/main/java/com/smartcity/pattern/flyweight/StreetlightProfileFactory.java",
        "tab_name": "StreetlightProfileFactory.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > flyweight > StreetlightProfileFactory",
        "start_line": 1,
        "end_line": 27,
        "out_img": r"screenshots\listing_5_1.png"
    },
    {
        "table_idx": 16,
        "listing_id": "Listing 6.1",
        "file": "backend/src/main/java/com/smartcity/pattern/interpreter/DslPolicyParser.java",
        "tab_name": "DslPolicyParser.java",
        "crumbs": "SmartCity360 > backend > src > main > java > com > smartcity > pattern > interpreter > DslPolicyParser",
        "start_line": 158,
        "end_line": 195,
        "out_img": r"screenshots\listing_6_1.png"
    }
]

print("=== GENERATING CODE IMAGES ===")
for meta in listings_meta:
    with open(meta["file"], "r", encoding="utf-8") as f:
        all_lines = f.readlines()
    code_slice = [l.rstrip() for l in all_lines[meta["start_line"] - 1 : meta["end_line"]]]
    render_code_window(
        meta["tab_name"],
        meta["crumbs"],
        code_slice,
        meta["start_line"],
        meta["out_img"]
    )

# ----------------- INSERT INTO DOCX -----------------
doc_path = r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx"
backup_path = r"docs\backup\SmartCity360_OODP_II_Final_Submission-v5.before_listings_insert.docx"
shutil.copyfile(doc_path, backup_path)
print(f"\nBacked up docx to: {backup_path}")

doc = docx.Document(doc_path)

print("=== INSERTING SCREENSHOTS INTO TABLES ===")
for meta in listings_meta:
    table = doc.tables[meta["table_idx"]]
    cell = table.rows[0].cells[0]
    
    # Add paragraph for the screenshot image
    p_img = cell.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(4)
    run_img = p_img.add_run()
    run_img.add_picture(meta["out_img"], width=Inches(6.2))
    
    print(f"Inserted {meta['out_img']} into Table {meta['table_idx']} ({meta['listing_id']})")

doc.save(doc_path)
print(f"Saved updated document to: {doc_path} ({os.path.getsize(doc_path)} bytes)")

# Synchronize other_files copy
shutil.copyfile(doc_path, r"other_files\SmartCity360_OODP_II_Final_Submission.docx")
print("Synchronized other_files copy.")

