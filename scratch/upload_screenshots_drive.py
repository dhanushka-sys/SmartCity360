import subprocess
import os

folder_id = "1SgUW_1sF2WeRh5zsNAgJvAxIWMYt62O0"
files = [
    r"screenshots\listing_2_1.png",
    r"screenshots\listing_3_1.png",
    r"screenshots\listing_4_1.png",
    r"screenshots\listing_5_1.png",
    r"screenshots\listing_6_1.png"
]

for f in files:
    cmd = f'gdrive mutate upload "{f}" --parent {folder_id}'
    print(f"Uploading {f}...")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(res.stdout.strip())

