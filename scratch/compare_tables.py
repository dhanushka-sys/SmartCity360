import docx

old_doc = docx.Document(r"docs/backup/SmartCity360_OODP_II_Final_Submission-v5.before_clean_listing_text.docx")
new_doc = docx.Document(r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx")

print(f"Old tables: {len(old_doc.tables)}, New tables: {len(new_doc.tables)}")

# Check table styles, borders, shading, cell properties for Table 4, Table 7, Table 24
for idx in [4, 7, 10, 13, 16, 24, 25]:
    old_t = old_doc.tables[idx]
    new_t = new_doc.tables[idx]
    print(f"\n--- TABLE {idx} ---")
    print(f"Old style: {old_t.style.name if old_t.style else 'None'}, New style: {new_t.style.name if new_t.style else 'None'}")
    print(f"Old cell xml:")
    print(old_t.cell(0, 0)._element.tcPr.xml if old_t.cell(0, 0)._element.tcPr is not None else "No tcPr")
    print(f"New cell xml:")
    print(new_t.cell(0, 0)._element.tcPr.xml if new_t.cell(0, 0)._element.tcPr is not None else "No tcPr")

