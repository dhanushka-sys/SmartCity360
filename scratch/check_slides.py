import json
import subprocess

res = subprocess.run('gslides readonly list-slides 1GAkU-MICbwrZLl8UaIKNKnfmZv0yNGVoG1s27p-lChA --json', capture_output=True, text=True, encoding='utf-8', shell=True)
data = json.loads(res.stdout)
for idx, slide in enumerate(data):
    title = 'No Title'
    for el in slide.get('pageElements', []):
        shape = el.get('shape', {})
        if shape.get('placeholder', {}).get('type') == 'TITLE':
            te = shape.get('text', {}).get('textElements', [])
            txt = ''.join([t.get('textRun', {}).get('content', '') for t in te]).strip()
            if txt:
                title = txt.split('\n')[0]
                break
    print(f"Slide {idx+1}: ID={slide['objectId']} | Title: {title}")
