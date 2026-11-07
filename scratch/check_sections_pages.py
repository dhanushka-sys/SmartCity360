import pymupdf

doc_curr = pymupdf.open(r"scratch/current.pdf")
doc_before = pymupdf.open(r"scratch/before.pdf")

headings = [
    "EXECUTIVE SUMMARY",
    "1. SYSTEM ARCHITECTURE",
    "2. PATTERN 1",
    "3. PATTERN 2",
    "4. PATTERN 3",
    "5. PATTERN 4",
    "6. PATTERN 5",
    "7. ENTERPRISE",
    "8. SUMMARY",
    "9. APPENDIX A"
]

print("=== CURRENT DOC PAGES ===")
for h in headings:
    for p_no in range(2, len(doc_curr)):
        text = doc_curr[p_no].get_text()
        if h in text.upper():
            print(f"Current: {h} -> Page {p_no + 1}")
            break

print("\n=== BEFORE DOC PAGES ===")
for h in headings:
    for p_no in range(2, len(doc_before)):
        text = doc_before[p_no].get_text()
        if h in text.upper():
            print(f"Before: {h} -> Page {p_no + 1}")
            break

