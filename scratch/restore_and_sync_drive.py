import shutil
import subprocess

src = r"scratch/restored_old_design.docx"
dest1 = r"docs/SmartCity360_OODP_II_Final_Submission-v5.docx"
dest2 = r"other_files/SmartCity360_OODP_II_Final_Submission.docx"

shutil.copy2(src, dest1)
shutil.copy2(src, dest2)
print("Copied restored design to docs/ and other_files/")

cmd = 'gdrive mutate update 1vO8Datj_N0OOtIaYl8zWTSK2JB5RAOsr "docs\\SmartCity360_OODP_II_Final_Submission-v5.docx"'
print(f"Running: {cmd}")
res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print(res.stdout.strip())
if res.stderr:
    print(f"Error: {res.stderr.strip()}")
print("Drive update complete.")

