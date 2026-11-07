import fitz # PyMuPDF
import os

doc_curr = fitz.open(r"scratch/current.pdf")
doc_before = fitz.open(r"scratch/before.pdf")

print(f"Current pages: {len(doc_curr)}, Before pages: {len(doc_before)}")

# Let's inspect pages around Section 2, 3, 4, 5, 6, 7 and Appendix A
# Find page of "9. Appendix A" or "APPENDIX A" in both
for p_no in range(len(doc_before)):
    text = doc_before[p_no].get_text()
    if "APPENDIX A" in text.upper():
        print(f"Before: Appendix A starts at Page {p_no + 1}")
        break

for p_no in range(len(doc_curr)):
    text = doc_curr[p_no].get_text()
    if "APPENDIX A" in text.upper():
        print(f"Current: Appendix A starts at Page {p_no + 1}")
        break

