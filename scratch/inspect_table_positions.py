import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

body_elements = doc._body._element
print(f"Total body children: {len(body_elements)}")

fig_tables = [2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 19, 20]
for t_idx in fig_tables:
    table = doc.tables[t_idx]
    tbl_elem = table._tbl
    parent = tbl_elem.getparent()
    idx = parent.index(tbl_elem)
    
    prev_txt = ""
    for i in range(idx-1, -1, -1):
        el = parent[i]
        if el.tag.endswith('p'):
            p_obj = docx.text.paragraph.Paragraph(el, doc)
            if p_obj.text.strip():
                prev_txt = p_obj.text.strip()
                break
                
    next_txt = ""
    for i in range(idx+1, len(parent)):
        el = parent[i]
        if el.tag.endswith('p'):
            p_obj = docx.text.paragraph.Paragraph(el, doc)
            if p_obj.text.strip():
                next_txt = p_obj.text.strip()
                break

    print(f"\nTable {t_idx} (child index {idx}):")
    print(f"  PREV P: {prev_txt[:80]}")
    print(f"  NEXT P: {next_txt[:80]}")

