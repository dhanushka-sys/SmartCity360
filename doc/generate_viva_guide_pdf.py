import os
import subprocess
import html
import shutil

def convert_markdown_to_guide_pdf():
    md_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "SmartCity360_Viva_and_Presentation_Guide.md")
    if not os.path.exists(md_path):
        md_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SmartCity360_Viva_and_Presentation_Guide.md")
    
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert simple markdown to formal HTML for Edge printing
    lines = md_text.split("\n")
    html_lines = []
    
    html_lines.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SmartCity360 — VIVA Oral Defense & Video Walkthrough Guide</title>
<style>
  @page {
    size: A4;
    margin: 20mm 16mm 20mm 16mm;
    @top-left {
      content: "SmartCity360 — Examination Companion & Defense Guide";
      font-family: 'Times New Roman', serif;
      font-size: 8.5pt;
      color: #64748b;
    }
    @top-right {
      content: "Unit ID: JIAT/OODP II | Part F Defense";
      font-family: 'Times New Roman', serif;
      font-size: 8.5pt;
      font-weight: bold;
      color: #1e3a8a;
    }
    @bottom-right {
      content: "Page " counter(page);
      font-family: 'Times New Roman', serif;
      font-size: 9pt;
      font-weight: bold;
    }
  }

  body {
    font-family: 'Times New Roman', Times, Georgia, serif;
    font-size: 10.5pt;
    line-height: 1.45;
    color: #1e293b;
    margin: 0;
    padding: 0;
  }

  h1 {
    font-size: 15pt;
    font-weight: bold;
    color: #0f294a;
    border-bottom: 2px solid #1e3a8a;
    padding-bottom: 4px;
    margin-top: 20px;
    margin-bottom: 12px;
    text-transform: uppercase;
  }

  h2 {
    font-size: 12.5pt;
    font-weight: bold;
    color: #1e3a8a;
    margin-top: 16px;
    margin-bottom: 8px;
    border-left: 3px solid #1e3a8a;
    padding-left: 8px;
  }

  h3 {
    font-size: 11pt;
    font-weight: bold;
    color: #0f294a;
    margin-top: 14px;
    margin-bottom: 6px;
    background: #f1f5f9;
    padding: 4px 8px;
    border-radius: 3px;
  }

  p {
    margin-top: 0;
    margin-bottom: 8px;
    text-align: justify;
  }

  blockquote {
    margin: 6px 0 12px 0;
    padding: 8px 12px;
    background: #f8fafc;
    border-left: 3.5px solid #059669;
    font-size: 10pt;
    color: #0f172a;
    border-radius: 0 4px 4px 0;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 14px 0;
    font-size: 9pt;
    page-break-inside: avoid;
  }

  th {
    background: #0f294a;
    color: #ffffff;
    font-weight: bold;
    text-align: left;
    padding: 6px 8px;
    border: 1px solid #0f294a;
  }

  td {
    padding: 5px 8px;
    border: 1px solid #cbd5e1;
  }

  tr:nth-child(even) td {
    background: #f8fafc;
  }

  code {
    font-family: 'Consolas', monospace;
    font-size: 9pt;
    background: #f1f5f9;
    color: #0f294a;
    padding: 1px 4px;
    border-radius: 2px;
  }

  pre {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    padding: 8px 10px;
    font-family: 'Consolas', monospace;
    font-size: 8.5pt;
    line-height: 1.3;
    overflow-x: auto;
    page-break-inside: avoid;
  }

  .badge {
    background: #e0f2fe;
    color: #0369a1;
    font-weight: bold;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 8.5pt;
  }

  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>
""")

    in_table = False
    in_code = False
    code_block = []

    for line in lines:
        if line.startswith("```"):
            if in_code:
                in_code = False
                html_lines.append(f"<pre><code>{html.escape(chr(10).join(code_block))}</code></pre>")
                code_block = []
            else:
                in_code = True
                code_block = []
            continue

        if in_code:
            code_block.append(line)
            continue

        if line.startswith("|") and line.endswith("|"):
            if not in_table:
                in_table = True
                html_lines.append("<table>")
            
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if all(c.startswith("---") or c == "" for c in cells):
                continue
            
            is_header = len(html_lines) > 0 and html_lines[-1] == "<table>"
            tag = "th" if is_header else "td"
            row = "".join([f"<{tag}>{html.escape(c)}</{tag}>" for c in cells])
            html_lines.append(f"<tr>{row}</tr>")
            continue
        else:
            if in_table:
                in_table = False
                html_lines.append("</table>")

        if line.startswith("# "):
            html_lines.append(f"<div style='border-bottom: 2.5px solid #0f294a; padding-bottom: 8px; margin-bottom: 16px;'>")
            html_lines.append(f"<div style='font-size: 8.5pt; font-weight: bold; color: #1e3a8a; text-transform: uppercase;'>JIAT / OODP II / EX / 01 &bull; Student Examination Guide</div>")
            html_lines.append(f"<h1 style='margin: 4px 0 2px 0; border: none; padding: 0;'>{html.escape(line[2:])}</h1>")
            html_lines.append("</div>")
        elif line.startswith("## "):
            html_lines.append(f"<h1>{html.escape(line[3:])}</h1>")
        elif line.startswith("### "):
            html_lines.append(f"<h2>{html.escape(line[4:])}</h2>")
        elif line.startswith("#### "):
            html_lines.append(f"<h3>{html.escape(line[5:])}</h3>")
        elif line.startswith("> "):
            quote_text = html.escape(line[2:])
            html_lines.append(f"<blockquote>{quote_text}</blockquote>")
        elif line.startswith("- "):
            html_lines.append(f"<p style='margin-left: 16px; margin-bottom: 4px;'>&bull; {html.escape(line[2:])}</p>")
        elif line.strip() == "---":
            html_lines.append("<hr style='border: none; border-top: 1px solid #cbd5e1; margin: 14px 0;'>")
        elif line.strip() == "":
            pass
        else:
            html_lines.append(f"<p>{html.escape(line)}</p>")

    if in_table:
        html_lines.append("</table>")

    html_lines.append("""
</body>
</html>
""")

    out_html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SmartCity360_Viva_and_Presentation_Guide.html")
    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

    # Convert to PDF via Edge
    root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    out_pdf_root = os.path.join(root_dir, "SmartCity360_Viva_and_Presentation_Guide.pdf")
    out_pdf_doc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SmartCity360_Viva_and_Presentation_Guide.pdf")

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_path):
        edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

    file_url = f"file:///{os.path.abspath(out_html_path).replace(os.sep, '/')}"
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={out_pdf_root}",
        file_url
    ]
    print("Executing PDF conversion for Viva Guide...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and os.path.exists(out_pdf_root):
        shutil.copyfile(out_pdf_root, out_pdf_doc)
        print(f"Successfully generated: {out_pdf_root} (Size: {os.path.getsize(out_pdf_root)} bytes)")
    else:
        print(f"Error generating PDF. Code: {result.returncode}, StdErr: {result.stderr}")

if __name__ == "__main__":
    convert_markdown_to_guide_pdf()

