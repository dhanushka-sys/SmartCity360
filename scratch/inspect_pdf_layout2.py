import pymupdf

doc_curr = pymupdf.open(r"scratch/current.pdf")
doc_before = pymupdf.open(r"scratch/before.pdf")

for p_no in range(len(doc_before)):
    text = doc_before[p_no].get_text()
    if "9. APPENDIX A" in text or "9.1 Part A" in text:
        print(f"Before: Appendix A body starts at Page {p_no + 1}")
        break

for p_no in range(len(doc_curr)):
    text = doc_curr[p_no].get_text()
    if "9. APPENDIX A" in text or "9.1 Part A" in text:
        print(f"Current: Appendix A body starts at Page {p_no + 1}")
        break

