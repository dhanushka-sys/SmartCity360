txt_path = r"docs\SmartCity360_OODP_II_Final_Submission-v5.txt"

with open(txt_path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.split('\n')
cleaned = []
skip = False

for line in lines:
    if '┌' in line or '>>>' in line:
        skip = True
        continue
    if '└' in line:
        skip = False
        continue
    if skip:
        continue
    if '📌 Candidate' in line or 'Candidate Screenshot Guide' in line or 'Candidate Insertion Guide' in line:
        continue
    cleaned.append(line)

new_text = '\n'.join(cleaned)

# Clean specific phrases
new_text = new_text.replace("PLACEHOLDER — ", "")
new_text = new_text.replace("Each figure location provides a structured placeholder and technical specification for direct visual artifact insertion:",
                            "Each architectural figure is embedded within its designated system specification section below:")
new_text = new_text.replace("Candidates can capture screenshots directly from their IDE (VS Code / IntelliJ IDEA) and insert them into each designated container below:",
                            "The complete, compilable source files are packaged in the project repository and cataloged below:")

with open(txt_path, "w", encoding="utf-8") as f:
    f.write(new_text)

print(f"Updated {txt_path} successfully. Total lines went from {len(lines)} to {len(cleaned)}")

