import subprocess

updates = [
    ("1Rb8Rkn1nfwy_YUal2BYGJWhjs9lPZ19b", r"screenshots\appendix\StreamData.java.png"),
    ("1kqwz3pWfqnGR7gJp69oqtTXQqiGH6AxT", r"screenshots\appendix\EnergyStreamData.java.png"),
    ("1glLM5E8zhW6ATuaHgIQyNbgMdYTyaQdW", r"screenshots\appendix\StreamDataDecorator.java.png"),
    ("1vO8Datj_N0OOtIaYl8zWTSK2JB5RAOsr", r"docs\SmartCity360_OODP_II_Final_Submission-v5.docx")
]

for file_id, path in updates:
    cmd = f'gdrive mutate update {file_id} "{path}"'
    print(f"Running: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(res.stdout.strip())
    if res.stderr:
        print(f"Error: {res.stderr.strip()}")

print("Drive synchronization completed.")

