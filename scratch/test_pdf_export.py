import os
import win32com.client
from pypdf import PdfReader

def docx_to_pdf(docx_path, pdf_path):
    word = win32com.client.DispatchEx('Word.Application')
    word.Visible = False
    try:
        abs_docx = os.path.abspath(docx_path)
        abs_pdf = os.path.abspath(pdf_path)
        doc = word.Documents.Open(abs_docx)
        doc.SaveAs2(abs_pdf, FileFormat=17) # 17 = wdFormatPDF
        doc.Close(False)
    finally:
        word.Quit()

docx_to_pdf(r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx", r"scratch/current.pdf")
reader = PdfReader(r"scratch/current.pdf")
print(f"Current document PDF page count: {len(reader.pages)}")

docx_to_pdf(r"docs/backup/SmartCity360_OODP_II_Final_Submission-v5.before_clean_listing_text.docx", r"scratch/before.pdf")
reader_before = PdfReader(r"scratch/before.pdf")
print(f"Before document PDF page count: {len(reader_before.pages)}")

