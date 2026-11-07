import os
import re
from PIL import Image, ImageDraw, ImageFont

BG_COLOR = (25, 26, 28)           # #191A1C IntelliJ New UI Editor BG
TAB_BAR_BG = (25, 26, 28)         # Same as editor
TAB_ACTIVE_BG = (35, 53, 88)      # Dark blue tab highlight
GUTTER_TEXT = (90, 95, 105)       # #5A5F69 Line numbers
TEXT_DEFAULT = (188, 190, 196)    # #BCBEC4 Identifiers / Punctuation
KW_COLOR = (207, 142, 109)        # #CF8E6D Orange keywords
STR_COLOR = (106, 171, 115)       # #6AAB73 Green strings
NUM_COLOR = (42, 172, 184)        # #2AACB8 Cyan numbers
COMMENT_COLOR = (122, 126, 133)   # #7A7E85 Grey comments
ANNOTATION_COLOR = (187, 181, 41) # #BBB529 Yellow annotations
TYPE_COLOR = (223, 225, 229)      # #DFE1E5 Light grey types
AUTHOR_COLOR = (105, 110, 120)    # Code vision usages / author
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

def render_intellij_windows_editor(filename, file_type, code_lines, start_line_num, out_png, usages_map=None):
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
    
    # Tab background
    draw.rounded_rectangle([(tab_x, tab_y), (tab_x + tab_w, tab_y + tab_h)], radius=4, fill=TAB_ACTIVE_BG)
    
    # Icon circle in tab (I for interface, C for class, E for enum)
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
        # Line number right aligned
        draw.text((gutter_width - 12 - len(line_no) * 9, curr_y), line_no, fill=GUTTER_TEXT, font=font)
        
        # Gutter override / implement icons
        if '@Override' in raw_line or 'public ' in raw_line and ('void ' in raw_line or 'String ' in raw_line or 'boolean ' in raw_line or 'int ' in raw_line or 'double ' in raw_line or 'ComplaintRoutingResult ' in raw_line):
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
            usages = usages_map.get(idx, "14 usages") if usages_map else "12 usages"
            vision_text = f"{usages}  👤 Dhanushka Maduranga"
            draw.text((curr_x + 18, curr_y + 2), vision_text, fill=AUTHOR_COLOR, font=vision_font)
        elif stripped.startswith('public ') and '(' in stripped and not stripped.startswith('public class') and not stripped.startswith('public interface'):
            usages = usages_map.get(idx, "6 usages") if usages_map else "5 usages"
            vision_text = f"{usages}  👤 Dhanushka Maduranga"
            draw.text((curr_x + 18, curr_y + 2), vision_text, fill=AUTHOR_COLOR, font=vision_font)
            
        curr_y += line_height
        
    img.save(out_png)
    print(f"Rendered Windows IntelliJ Screenshot: {out_png} ({width}x{height})")

if __name__ == "__main__":
    with open("backend/src/main/java/com/smartcity/pattern/decorator/CompressionDecorator.java", "r") as f:
        lines = [l.rstrip() for l in f.readlines()[:38]]
    render_intellij_windows_editor("CompressionDecorator.java", "class", lines, 1, "scratch/test_windows_compression.png")

