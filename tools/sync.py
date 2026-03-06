import json
from pathlib import Path

ORIGINAL_JSON_PATH = Path('./data/original_json')
TRANSLATED_JSON_PATH = Path('./data/translated_json')

for t in TRANSLATED_JSON_PATH.rglob('*.json'):
    rel = t.relative_to(TRANSLATED_JSON_PATH)
    o = ORIGINAL_JSON_PATH / rel
    if not o.exists():
        print(f'Warning: {o} does not exits')
        continue

    with open(o, 'r') as f:
        original = json.load(f)
    with open(t, 'r') as f:
        translated = json.load(f)

    assert len(original) == len(translated), t

    for i in range(len(original)):
        translated[i]['original'] = original[i]['original']
        translated[i]['name'] = original[i]['name']

    with open(t, 'w') as f:
        json.dump(translated, f, indent=2, ensure_ascii=False)
