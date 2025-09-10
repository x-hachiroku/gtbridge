import os
import re
import json
from pathlib import Path

from gtbridge import load


scenario_dir = Path('./data/scenario')
ks_files = scenario_dir.rglob('*.ks')

for ks_file in ks_files:
    relative_path = ks_file.relative_to(scenario_dir)
    ks_basename = str(relative_path)

    with open(ks_file) as f:
        lines = f.read().splitlines()

    translated_json_path = Path('./data/translated_json/') / f'{ks_basename}.json'
    if translated_json_path.exists():
        translated_messages = load(str(translated_json_path))

        for translated_message in translated_messages:
            if isinstance(translated_message.tags[0], int):
                lines[translated_message.tags[0]] = translated_message.message
            else:
                raise NotImplementedError('Unexpected tag type.')
        script = '\n'.join(lines)

        output_file = Path(f'./data/translated_ks/{ks_basename}')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-16') as f:
            f.write(script)
