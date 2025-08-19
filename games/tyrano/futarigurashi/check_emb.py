import re
import json
from glob import glob

EMB_PATTERN = re.compile(r'\[emb exp=[^\]]+\]')

for t in glob('./data/translated_json/**/*.json', recursive=True):
    with open(t, 'r') as f:
        translated = json.load(f)

    for i in translated:
        matches = EMB_PATTERN.findall(i['message'])
        if len(matches) > 1:
            print(i['original'])
            print(i['message'])
            print()
        for match in matches:
            assert i['original'].count(match) == i['message'].count(match), \
                    f"Mismatch in {t}:\n{i['original']}\n{i['message']}"
