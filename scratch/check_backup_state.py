import docx

doc = docx.Document(r"docs/backup/SmartCity360_OODP_II_Final_Submission-v5.before_clean_listing_text.docx")
print("=== BEFORE CLEAN LISTING TEXT ===")
print(f"Total tables: {len(doc.tables)}, paragraphs: {len(doc.paragraphs)}")

# Check Table 4 (Listing 2.1)
print(f"Table 4 text: {doc.tables[4].cell(0, 0).text[:100]}")
# Check Table 24 (Appendix A.1.1)
print(f"Table 24 text: {doc.tables[24].cell(0, 0).text[:100]}")

