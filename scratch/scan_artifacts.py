import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

keywords = [
    "┌", "└", ">>>", "PASTE", "INSERT YOUR", "Candidate", 
    "Recommended Canvas Dimensions", "Recommended IDE View", 
    "Supported Formats", "PLACEHOLDER", "Assessment Mapping", 
    "Diagram Category", "Key Architectural Elements", 
    "Specifications to Include", "ARCHITECTURAL SPECIFICATION",
    "Candidate Screenshot Guide", "Candidate Insertion Guide"
]

print("=== SCANNING TABLES FOR USELESS TEMPLATE ARTIFACTS ===")
for t_idx, table in enumerate(doc.tables):
    found = []
    text = ""
    for r in table.rows:
        for c in r.cells:
            text += c.text + " "
    for kw in keywords:
        if kw.lower() in text.lower():
            found.append(kw)
    if found:
        print(f"Table {t_idx:2d} has artifacts: {found}")

print("\n=== SCANNING PARAGRAPHS FOR USELESS TEMPLATE ARTIFACTS ===")
for p_idx, p in enumerate(doc.paragraphs):
    found = []
    for kw in keywords:
        if kw.lower() in p.text.lower():
            found.append(kw)
    if found:
        print(f"Paragraph {p_idx:3d} has artifacts: {found} -> {p.text[:80]}")

