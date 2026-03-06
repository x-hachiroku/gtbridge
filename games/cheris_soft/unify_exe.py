import json
from pathlib import Path

with open('./data/exe.json') as f:
    exe_data = json.load(f)

exe_dict = {i['original']: i['message'] for i in exe_data}

for tj in Path('./data/translated_json/').rglob('*.tag.json'):
    tjd = json.loads(tj.read_text())
    for l in tjd:
        if l['original'] in exe_dict:
            l['message']= '「' + exe_dict[l['original']] + '」'
            l['pre'] = ''
            l['post'] = ''

    tj.write_text(json.dumps(tjd, ensure_ascii=False, indent=2))
