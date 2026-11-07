import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

print(f"Total paragraphs: {len(doc.paragraphs)}")
print(f"Total tables: {len(doc.tables)}")

placeholders = []
for idx, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if "PLACEHOLDER" in txt.upper() or "FIGURE" in txt.upper() or "LISTING" in txt.upper():
        if any(keyword in txt for keyword in ["PLACEHOLDER", "[ Figure", "[Figure", "📷", "Listing"]):
            placeholders.append((idx, txt))

print(f"Found {len(placeholders)} matching paragraphs:")
for idx, txt in placeholders[:40]:
    print(f"P[{idx}]: {txt}")

