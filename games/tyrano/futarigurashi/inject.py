import os
import re
import json
from pathlib import Path

from gtbridge import load


scenario_dir = Path('./data/app/data/scenario')
ks_files = scenario_dir.rglob('*.ks')

for ks_file in ks_files:
    relative_path = ks_file.relative_to(scenario_dir)
    ks_basename = str(relative_path)

    with open(ks_file) as f:
        lines = f.read().splitlines()

    translated_json_path = Path(f'./data/translated_json/{ks_basename}.json')
    if translated_json_path.exists():
        translated_messages = load(str(translated_json_path))

        for translated_message in translated_messages:
            if len(translated_message.tags) == 2 and isinstance(translated_message.tags[0], int):
                start, end = translated_message.tags
                lines[start] = translated_message.message
                while start < end:
                    start += 1
                    lines[start] = ''
        script = '\n'.join(lines)

        for translated_message in translated_messages:
            if 'TIPS' in translated_message.tags:
                o_subject, o_text = translated_message.original.split('\n', 1)
                t_subject, t_text = translated_message.message.split('\n', 1)
                translated_message.original = f'[showTips subject="{o_subject}" text="{o_text}"]'
                translated_message.message = f'[showTips subject="{t_subject}" text="{t_text}"]'
            script = script.replace(translated_message.original, translated_message.message)

        output_file = Path(f'./data/translated_ks/{ks_basename}')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(script)
