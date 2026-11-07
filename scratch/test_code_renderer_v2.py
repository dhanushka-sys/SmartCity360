import os
import re
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
    tab_w = 260
    draw.rectangle([(tab_x, 5), (tab_x + tab_w, top_bar_height)], fill=TAB_ACTIVE_BG)
    draw.line([(tab_x, 5), (tab_x + tab_w, 5)], fill=(53, 116, 240), width=2)
    draw.text((tab_x + 14, 11), filename, fill=(223, 225, 229), font=title_font)
    draw.text((tab_x + tab_w - 22, 11), "×", fill=(134, 137, 144), font=title_font)
    
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
        if ('class ' in raw_line or 'interface ' in raw_line) and not first_class_found:
            first_class_found = True
            draw.text((curr_x + 25, curr_y + 3), "Dhanushka Maduranga", fill=AUTHOR_COLOR, font=vision_font)
            
        curr_y += line_height
        
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline=BORDER_COLOR, width=1)
    img.save(out_png)
    print(f"Rendered: {out_png} ({width}x{height})")

if __name__ == "__main__":
    with open("backend/src/main/java/com/smartcity/pattern/decorator/StreamData.java", "r") as f:
        lines = [l.rstrip() for l in f.readlines()]
    render_code_window("StreamData.java", "SmartCity360 > backend > src > main > java > com > smartcity > pattern > decorator > StreamData", lines, 1, "scratch/test_stream_data.png")

