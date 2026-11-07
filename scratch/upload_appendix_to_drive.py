import os
import subprocess

screenshots_folder_id = "1SgUW_1sF2WeRh5zsNAgJvAxIWMYt62O0"
appendix_dir = r"screenshots\appendix"

for f in os.listdir(appendix_dir):
    if f.endswith(".png"):
        local_path = os.path.join(appendix_dir, f)
        print(f"Uploading {f}...")
        cmd = f'gdrive mutate upload "{local_path}" --parent {screenshots_folder_id}'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(res.stdout.strip())

print("All appendix screenshots uploaded.")

