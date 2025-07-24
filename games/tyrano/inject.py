import os
import re
import json
from glob import glob
from pathlib import Path
from message import load


NAME_PATTERN = re.compile(
    r'(\[chara_new\s+' + \
    r'name="([^"]+)"\s+)' + \
    r'jname="[^"]+"\s+' + \
    r'([^\]]+\])'
)

with open('./names.json'):
    names = json.load(open('./names.json'))

for ks in glob('./data/app/data/scenario/**/*.ks', recursive=True):
    ks_basename = '/'.join(ks.split('/')[5:])
    with open(ks) as f:
        script = f.read()

    ## yuukai
    i = 0
    while True:
        if not os.path.exists(f'./data/translated_json/{ks_basename}.extra{i:02d}.json'):
            break

        translated_messages = load(f'./data/translated_json/{ks_basename}.extra{i:02d}.json')

        original_list_str = str(list(map(lambda x: x.original, translated_messages)))
        translated_list_str = str(list(map(lambda x: x.message, translated_messages)))
        assert original_list_str in script, \
                f'Original list string not found in {ks_basename}: {original_list_str}'
        script = script.replace(original_list_str, translated_list_str)
        i += 1

    ## Names
    for match in NAME_PATTERN.finditer(script):
        name = match.group(2)
        chara_new = match.group(1) + f'jname="{names[name]}"  ' + match.group(3)
        script = script.replace(match.group(0), chara_new)
        i += 1

    ## Messages
    if os.path.exists(f'./data/translated_json/{ks_basename}.json'):
        translated_messages = load(f'./data/translated_json/{ks_basename}.json')
        for translated_message in translated_messages:
            assert translated_message.original in script, \
                    f'Original message not found in {ks_basename}: {translated_message.original}'
            script = script.replace(translated_message.original, translated_message.message, 1)
        i+=1

    if i > 0:
        filepath = Path(f'./data/translated_ks/{ks_basename}')
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(script)
