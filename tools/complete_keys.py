import json
from pathlib import Path

for src in Path('.').rglob('*.json'):
    with open(src) as f:
        data = json.load(f)
    for message in data:
        if 'name' not in message:
            message['name'] = None
        if 'pre' not in message:
            message['pre'] = None
        if 'post' not in message:
            message['post'] = None
        if 'original' not in message:
            message['original'] = message['message']

    with open(src, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
