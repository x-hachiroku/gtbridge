from pathlib import Path
from gtbridge import load

with open('gpt-dict.txt') as f:
    gpt_dict = dict(line.split('\t')[:2] for line in f.read().splitlines() if line)

for path in Path('./data/translated_json').rglob('*.json'):
    messages = load(path)
    for message in messages:
        for key, value in gpt_dict.items():
            if key in message.original and value not in message.message:
                print(f'{path}: {key}\n{message.original}\n{message.message}\n')
