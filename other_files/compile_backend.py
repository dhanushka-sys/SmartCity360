import glob
import os
import subprocess

all_files = glob.glob('backend/src/main/java/**/*.java', recursive=True)

os.makedirs('backend/target/classes', exist_ok=True)
with open('backend/all_sources.txt', 'w', encoding='utf-8') as f:
    for file in all_files:
        f.write('"' + file.replace('\\', '/') + '"\n')

cp_separator = ';' if os.name == 'nt' else ':'
classpath = f"backend/src/main/java{cp_separator}backend/lib/*"

cmd = f'javac -d backend/target/classes -cp "{classpath}" @backend/all_sources.txt'
res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print('Compilation exit code:', res.returncode)
if res.stdout:
    print('STDOUT:\n', res.stdout)
if res.stderr:
    print('STDERR:\n', res.stderr)
if res.returncode == 0:
    print(f'ALL {len(all_files)} BACKEND JAVA FILES (Controllers, DAOs, Filters, Patterns, Models, Tests) COMPILED SUCCESSFULLY WITH ZERO ERRORS!')
