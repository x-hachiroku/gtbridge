import os
import re
import json
from pathlib import Path
from gtbridge import load


NAME_PATTERN = re.compile(
    r'(\[chara_new\s+' + \
    r'name="([^"]+)"\s+)' + \
    r'jname="[^"]+"\s+' + \
    r'([^\]]+\])'
)

with open('./names.json') as f:
    names = json.load(f)

scenario_dir = Path('./data/app/data/scenario')
ks_files = scenario_dir.rglob('*.ks')

for ks_file in ks_files:
    relative_path = ks_file.relative_to(scenario_dir)
    ks_basename = str(relative_path)

    with open(ks_file) as f:
        script = f.read()

    ## yuukai
    i = 0
    while True:
        extra_json_path = Path(f'./data/translated_json/{ks_basename}.extra{i:02d}.json')
        if not extra_json_path.exists():
            break

        translated_messages = load(str(extra_json_path))

        original_list_str = str(list(map(lambda x: x.original, translated_messages)))
        translated_list_str = str(list(map(lambda x: x.message, translated_messages)))
        assert original_list_str in script, \
                f'Original list string not found in {ks_basename}: {original_list_str}'
        script = script.replace(original_list_str, translated_list_str)
        i += 1

    ## Names
    for match in NAME_PATTERN.finditer(script):
        name = match.group(2)
        if name not in names:
            print(f'Warning: Name "{name}" not found for {ks_basename}. Skipping...')
            continue
        chara_new = match.group(1) + f'jname="{names[name]}"  ' + match.group(3)
        script = script.replace(match.group(0), chara_new)
        i += 1

    ## Messages
    translated_json_path = Path(f'./data/translated_json/{ks_basename}.json')
    if translated_json_path.exists():
        translated_messages = load(str(translated_json_path))
        for translated_message in translated_messages:
            if 'TIPS' in translated_message.tags:
                o_subject, o_text = translated_message.original.split('\n', 1)
                t_subject, t_text = translated_message.message.split('\n', 1)
                translated_message.original = f'[showTips subject="{o_subject}" text="{o_text}"]'
                translated_message.message = f'[showTips subject="{t_subject}" text="{t_text}"]'
            assert translated_message.original in script, \
                    f'Original message not found in {ks_basename}: {translated_message.original}'
            script = script.replace(translated_message.original, translated_message.message, 1)
        i+=1

    if i > 0:
        output_file = Path(f'./data/translated_ks/{ks_basename}')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(script)
