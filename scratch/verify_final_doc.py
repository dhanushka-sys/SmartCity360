import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

fig_tables = [2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 19, 20]

print(f"Total tables: {len(doc.tables)}")

for t_idx in fig_tables:
    table = doc.tables[t_idx]
    cell = table.rows[0].cells[0]
    paras = cell.paragraphs
    has_image = False
    image_rId = None
    for p in paras:
        for r in p.runs:
            blips = r._r.xpath('.//a:blip/@r:embed')
            if blips:
                has_image = True
                image_rId = blips[0]
    first_line = paras[0].text.split('\n')[0] if paras else "EMPTY"
    caption_line = paras[-1].text if len(paras) > 1 else "NO CAPTION"
    print(f"Table {t_idx:2d}: Image={has_image} (rId: {image_rId}) | Header: {first_line} | Caption: {caption_line}")

