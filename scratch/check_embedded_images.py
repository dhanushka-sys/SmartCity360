import docx

doc = docx.Document(r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx")

for idx in range(2, 21):
    tbl = doc.tables[idx]
    cell = tbl.cell(0, 0)
    # find blip r:embed
    blips = cell._element.xpath('.//a:blip/@r:embed')
    for b in blips:
        part = doc.part.related_parts[b]
        print(f"Table {idx}: part {part.partname}, size {len(part.blob)} bytes")

