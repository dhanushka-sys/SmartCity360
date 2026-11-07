import docx

doc = docx.Document('docs/SmartCity360_OODP_II_Final_Submission-v5.docx')

t24 = doc.tables[24]._element
parent = t24.getparent()
idx = parent.index(t24)
print(f'Table 24 index in body: {idx}')
for i in range(max(0, idx - 5), min(len(parent), idx + 10)):
    el = parent[i]
    if el.tag.endswith('p'):
        p = docx.text.paragraph.Paragraph(el, doc)
        print(f'[{i}] Paragraph: {p.text[:90]}')
    elif el.tag.endswith('tbl'):
        tbl_idx = [x._element for x in doc.tables].index(el)
        first_txt = el.xpath('.//w:t')
        t_str = first_txt[0].text if first_txt else 'empty'
        print(f'[{i}] Table {tbl_idx}: {t_str[:60]}')

