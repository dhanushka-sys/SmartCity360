import docx

doc = docx.Document(r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx")

for i, p in enumerate(doc.paragraphs):
    pPr = p._element.pPr
    if pPr is not None:
        pb = pPr.find(docx.oxml.ns.qn('w:pageBreakBefore'))
        if pb is not None:
            print(f"P{i}: pbBefore=True | {p.text.strip()[:60]}")

