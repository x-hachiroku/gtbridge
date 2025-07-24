import sys
import json
from pathlib import Path

for j in Path('./data/translated_json').rglob('*.json'):
    with open(j, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        item['message'] = item['message'].replace(sys.argv[1], sys.argv[2])

    with open(j, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
