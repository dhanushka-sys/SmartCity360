import pymupdf

doc = pymupdf.open(r"scratch/current.pdf")

print("=== CHECKING ALL PAGES 1 TO 44 ===")
for p_no in range(44):
    page = doc[p_no]
    rect = page.rect
    text = page.get_text().strip()
    imgs = page.get_images()
    lines = [l for l in text.split('\n') if l.strip()]
    first_line = lines[0] if lines else 'EMPTY'
    last_line = lines[-1] if lines else 'EMPTY'
    # Check if a heading is near bottom
    has_orphan_heading = False
    for l in lines[-4:]:
        if any(l.startswith(prefix) for prefix in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.']):
            has_orphan_heading = True
    print(f"Page {p_no+1:2d}: imgs={len(imgs)}, lines={len(lines):2d} | top: {first_line[:40]} | bottom: {last_line[:40]} {'<-- ORPHAN HEADING!' if has_orphan_heading else ''}")

