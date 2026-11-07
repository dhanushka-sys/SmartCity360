import docx

doc_before = docx.Document(r"docs/backup/SmartCity360_OODP_II_Final_Submission-v5.before_clean_listing_text.docx")
doc_now = docx.Document(r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx")

print(f"Before: {len(doc_before.paragraphs)} paragraphs, {len(doc_before.tables)} tables")
print(f"Now:    {len(doc_now.paragraphs)} paragraphs, {len(doc_now.tables)} tables")

# Check paragraph count differences
for i in range(min(len(doc_before.paragraphs), len(doc_now.paragraphs))):
    p_b = doc_before.paragraphs[i].text.strip()
    p_n = doc_now.paragraphs[i].text.strip()
    if p_b != p_n:
        print(f"Diff at P{i}:")
        print(f"  Before: {p_b[:80]}")
        print(f"  Now:    {p_n[:80]}")
        break

