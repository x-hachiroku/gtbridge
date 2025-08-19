import re
import json
from glob import glob

EMB_PATTERN = re.compile(r'\[emb exp=[^\]]+\]')

for j in glob('**/*.json', recursive=True):
    with open(j, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        for emb in EMB_PATTERN.findall(item['original']):
            if item['original'].count(emb) != item['message'].count(emb):
                print(f"Error in {j}: {emb}\n{item['original']}\n{item['message']}\n")
