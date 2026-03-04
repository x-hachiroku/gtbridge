import json
from pathlib import Path

keys = ()
for c in Path('.').glob("*.json"):
    data = json.loads(c.read_text())
    for l in data:
        for key in keys:
            if key in l['pre_jp']:
                l['problem'] = 'force'

    c.write_text(json.dumps(data, ensure_ascii=False, indent=2))
