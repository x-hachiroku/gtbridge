import json
from pathlib import Path

names = {}
for v in Path('./data/original_json/main/').glob('_v*.json'):
    meta = v.stem
    name = json.loads(v.read_text())[0]['original']
    names[meta] = name


print(json.dumps(names, indent=2, ensure_ascii=False))
