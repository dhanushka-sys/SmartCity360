import docx

doc = docx.Document(r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")

for idx, p in enumerate(doc.paragraphs[:75]):
    if "EXECUTIVE SUMMARY" in p.text.upper() or "SCENARIO OVERVIEW" in p.text.upper():
        print(f"Found at P[{idx}]: {p.text}")
        for j in range(idx, min(idx + 10, len(doc.paragraphs))):
            print(f"  P[{j}]: {doc.paragraphs[j].text[:80]}")

