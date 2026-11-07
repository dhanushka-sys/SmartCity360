import pymupdf

doc = pymupdf.open(r"scratch/current.pdf")

for p_no in range(len(doc)):
    page = doc[p_no]
    image_list = page.get_images()
    if image_list:
        text = page.get_text()[:120].replace('\n', ' ')
        print(f"Page {p_no + 1}: {len(image_list)} images | text: {text}")

