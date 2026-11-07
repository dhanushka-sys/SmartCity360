import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

fig_tables = [2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 19, 20]

for t_idx in fig_tables:
    table = doc.tables[t_idx]
    text = table.rows[0].cells[0].text
    lines = text.split('\n')
    header_lines = []
    box_lines = []
    footer_lines = []
    mode = 'header'
    for line in lines:
        if '┌' in line:
            mode = 'box'
        elif '📌' in line or 'Candidate Insertion' in line:
            mode = 'footer'
        
        if mode == 'header':
            header_lines.append(line)
        elif mode == 'box':
            box_lines.append(line)
        elif mode == 'footer':
            footer_lines.append(line)
            
    print(f"Table {t_idx}: Header lines: {len(header_lines)}, Box lines: {len(box_lines)}, Footer lines: {len(footer_lines)}")
    print(f"   Header[0]: {header_lines[0] if header_lines else ''}")
    print(f"   Header[1]: {header_lines[1] if len(header_lines) > 1 else ''}")

