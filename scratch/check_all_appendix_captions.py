import docx

doc = docx.Document('docs/SmartCity360_OODP_II_Final_Submission-v5.docx')

for idx in range(24, len(doc.tables)):
    t = doc.tables[idx]._element
    parent = t.getparent()
    p_idx = parent.index(t)
    next_p = parent[p_idx + 1]
    p_obj = docx.text.paragraph.Paragraph(next_p, doc)
    print(f"Table {idx} next paragraph: '{p_obj.text}'")

