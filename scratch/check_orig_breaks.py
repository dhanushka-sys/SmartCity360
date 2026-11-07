import docx

orig_doc = docx.Document(r"docs/backup/SmartCity360_OODP_II_Final_Submission-v2.original.docx")
print("=== ORIGINAL DOC SECTIONS / PAGE BREAKS ===")
for i, p in enumerate(orig_doc.paragraphs):
    # check if paragraph has page break
    has_pb = any('page' in r._element.xml for r in p.runs)
    if 'Part ' in p.text or 'Executive Summary' in p.text or 'APPENDIX' in p.text:
        print(f"P{i} (pb={has_pb}): {p.text.strip()[:80]}")

