import os
import sys
import json

for j in os.listdir('./'):
    if j.endswith('.json'):
        with open(j, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            item['message'] = item['message'].replace(sys.argv[1], sys.argv[2])

        with open(j, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
