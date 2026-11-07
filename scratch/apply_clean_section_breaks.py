import docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
import shutil

doc_path = r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx"
doc = docx.Document(doc_path)

# First, remove ALL pageBreakBefore elements from all paragraphs
for p in doc.paragraphs:
    pPr = p._element.pPr
    if pPr is not None:
        pb = pPr.find(qn('w:pageBreakBefore'))
        if pb is not None:
            pPr.remove(pb)

def add_pb(p):
    pPr = p._element.get_or_add_pPr()
    pb = OxmlElement('w:pageBreakBefore')
    pPr.append(pb)

# Find exact target paragraphs for major section starts
# 1. Table of Contents
# 2. Executive Summary (Body start)
# 3. Part A
# 4. Part B
# 5. Part C
# 6. Part D
# 7. Part E
# 8. Part F
# 9. Conclusion
# 10. Appendix A

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    # P4 is TABLE OF CONTENTS
    if i == 4 and "TABLE OF CONTENTS" in text:
        add_pb(p)
        print(f"P{i}: TOC Page Break")
    # Body sections (after P60, so after TOC and Tables of Figures/Listings)
    elif i > 60:
        if text.startswith("1. Executive Summary") or text.startswith("1.0 Executive Summary"):
            add_pb(p)
            print(f"P{i}: Section 1 Page Break")
        elif text.startswith("2. Part A"):
            add_pb(p)
            print(f"P{i}: Section 2 Page Break")
        elif text.startswith("3. Part B"):
            add_pb(p)
            print(f"P{i}: Section 3 Page Break")
        elif text.startswith("4. Part C"):
            add_pb(p)
            print(f"P{i}: Section 4 Page Break")
        elif text.startswith("5. Part D"):
            add_pb(p)
            print(f"P{i}: Section 5 Page Break")
        elif text.startswith("6. Part E"):
            add_pb(p)
            print(f"P{i}: Section 6 Page Break")
        elif text.startswith("7. Part F") or text.startswith("7. Final Project Demonstration"):
            add_pb(p)
            print(f"P{i}: Section 7 Page Break")
        elif text.startswith("8. Conclusion"):
            add_pb(p)
            print(f"P{i}: Section 8 Page Break")
        elif "9. APPENDIX A" in text:
            add_pb(p)
            print(f"P{i}: Appendix A Page Break")

doc.save(doc_path)
print("Saved clean page breaks.")
shutil.copy2(doc_path, r"other_files/SmartCity360_OODP_II_Final_Submission.docx")

