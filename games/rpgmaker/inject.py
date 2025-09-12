import json
from tqdm import tqdm
from pathlib import Path
from gtbridge import load

raw_dir = Path('./data/raw')
base_dir = Path('./data')

strs = {}
for s in load('./data/translated.json'):
    strs[s.original] = s.message

def process_list(l):
    for cmd in l:
        if cmd['code'] in {101, 401}:
            cmd['parameters'][0] = strs[cmd['parameters'][0]]
        elif cmd['code'] == 102:
            for i in range(len(cmd['parameters'][0])):
                cmd['parameters'][0][i] = strs[cmd['parameters'][0][i]]
        elif cmd['code'] == 402:
            cmd['parameters'][1] = strs[cmd['parameters'][1]]

for j in tqdm(list(raw_dir.rglob('*.json'))):
    relative_path = j.relative_to(raw_dir)
    with open(j, 'r') as f:
        d = json.load(f)

    for j in raw_dir.rglob('*.json'):
        with open(j, 'r') as f:
            db = json.load(f)

        if isinstance(db, list):
            for page in db:
                if page and 'list' in page:
                    process_list(page['list'])

        elif isinstance(db, dict) and 'events' in db:
            for event in db['events']:
                if event and 'pages' in event:
                    for page in event['pages']:
                        if page and 'list' in page:
                            process_list(page['list'])

    out_path = base_dir / 'translated' / relative_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
