import sys
import json
from glob import glob

key, val = sys.argv[1], sys.argv[2]
for j in glob('**/*.json', recursive=True):
    with open(j, 'r') as f:
        data = json.load(f)

    for msg in data:
        if key in msg['original']:
            if val not in msg['message']:
                print(f'{j}: "{msg["original"]}" -> "{msg["message"]}"')
