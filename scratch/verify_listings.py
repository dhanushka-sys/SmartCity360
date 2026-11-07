import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

listing_tables = [
    (4, "Listing 2.1", "EncryptionDecorator.java"),
    (7, "Listing 3.1", "ZoneComposite.java"),
    (10, "Listing 4.1", "ComplaintHandler.java"),
    (13, "Listing 5.1", "StreetlightProfileFactory.java"),
    (16, "Listing 6.1", "DslPolicyParser.java"),
]

print("=== VERIFYING LISTING TABLES ===")
for t_idx, listing_id, file_name in listing_tables:
    table = doc.tables[t_idx]
    cell = table.rows[0].cells[0]
    
    has_image = False
    for p in cell.paragraphs:
        for r in p.runs:
            if r._r.xpath('.//a:blip'):
                has_image = True
                break
                
    parent = table._tbl.getparent()
    idx = parent.index(table._tbl)
    next_p = docx.text.paragraph.Paragraph(parent[idx+1], doc)
    
    print(f"Table {t_idx:2d} | {listing_id} ({file_name}): Has Image = {has_image}")
    print(f"   Cell P[0]: {cell.paragraphs[0].text[:60]}")
    print(f"   Caption:   {next_p.text[:70]}")

