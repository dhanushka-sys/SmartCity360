import glob
import os
import subprocess

pattern_files = glob.glob('backend/src/main/java/com/smartcity/pattern/**/*.java', recursive=True)
model_files = glob.glob('backend/src/main/java/com/smartcity/model/**/*.java', recursive=True)
test_files = glob.glob('backend/src/main/java/com/smartcity/test/**/*.java', recursive=True)
all_files = pattern_files + model_files + test_files

os.makedirs('backend/target/classes', exist_ok=True)
with open('backend/pattern_sources.txt', 'w', encoding='utf-8') as f:
    for file in all_files:
        f.write('"' + file.replace('\\', '/') + '"\n')

cmd = 'javac -d backend/target/classes -cp "backend/src/main/java" @backend/pattern_sources.txt'
res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print('Pattern compilation exit code:', res.returncode)
if res.stdout:
    print('STDOUT:\n', res.stdout)
if res.stderr:
    print('STDERR:\n', res.stderr)
if res.returncode == 0:
    print('ALL 5 PATTERNS COMPILED SUCCESSFULLY WITH ZERO ERRORS!')
