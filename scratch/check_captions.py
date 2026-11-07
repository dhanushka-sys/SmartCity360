import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

fig_tables = [2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 19, 20]
for t_idx in fig_tables:
    table = doc.tables[t_idx]
    tbl_elem = table._tbl
    parent = tbl_elem.getparent()
    idx = parent.index(tbl_elem)
    
    next_p = ""
    for i in range(idx+1, len(parent)):
        el = parent[i]
        if el.tag.endswith('p'):
            p_obj = docx.text.paragraph.Paragraph(el, doc)
            if p_obj.text.strip():
                next_p = p_obj.text.strip()
                break
                
    print(f"Table {t_idx:2d} -> NEXT P: {next_p}")

