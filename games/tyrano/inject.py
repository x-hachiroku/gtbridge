import re
import json
import itertools
from pathlib import Path

from gtbridge import load
from extract import MESSAGE_PATTERN, PTEXT_PATTERN, EVAL_TEXT_PATTERN, CONDITION_TEXT_PATTERN, MESSAGE_LIST_PATTERN


VONAME_PATTERN = re.compile(
    r'\[(?:voconfig)(?=\s+)'
    r'.*?'
    r'name="([^"]+)"\s+'
    r'.*?'
    r'\]'
)

with open('./names.json') as f:
    names = json.load(f)

original_scenario_dir = Path('./data/original/data/scenario')
translated_scenario_dir = Path('./data/translated/data/scenario')
translated_json_dir = Path('./data/translated_json')


def name_replacer(match):
    name = match.group(1)
    if name not in names:
        print(f'Warning: Name "{name}" not found for {original_ks_path.name}, skipping...')
        return match.group(0)
    return match.group(0).replace(name, names[name])

def message_replacer(match):
    if "replace('あ" in match.group(0):
        next(translated_messages)
        return match.group(0)

    translated_message = next(translated_messages)
    assert translated_message.original == match.group(0), (translated_message, match.group(0))

    for tag in translated_message.tags:
        if tag.startswith('TAG:'):
            _tag = tag[4:]
            assert _tag in translated_message.message, translated_message

    if original_name := match.groupdict().get('name'):
        name = names[original_name]
        translated_message.message = translated_message.message.replace(original_name, name)

    return translated_message.message

def message_list_replacer(match):
    original_list_str = ', '.join(match.group(0).split())
    assert original_list_str == match.group(0)
    translated_list_str = ', '.join(match.group(0).split())
    return translated_list_str

for original_ks_path in original_scenario_dir.rglob('*.ks'):
    ks_relative_path = original_ks_path.relative_to(original_scenario_dir)
    translated_ks_file = translated_scenario_dir / ks_relative_path
    translated_ks_file.parent.mkdir(parents=True, exist_ok=True)
    translated_json_path = translated_json_dir / ks_relative_path.with_suffix('.json')
    script = original_ks_path.read_text()

    ## Messages
    if translated_json_path.exists():
        translated_messages = iter(load(str(translated_json_path)))
        script = MESSAGE_PATTERN.sub(message_replacer, script)
        script = PTEXT_PATTERN.sub(message_replacer, script)
        script = EVAL_TEXT_PATTERN.sub(message_replacer, script)
        script = CONDITION_TEXT_PATTERN.sub(message_replacer, script)
        _SENTINEL = object()
        assert next(translated_messages, _SENTINEL) is _SENTINEL

    ## Message Lists
    for translated_list_json_path in translated_json_dir.rglob(f'{ks_relative_path.stem}.message_list_*.json'):
        translated_messages = iter(load(str(translated_list_json_path)))
        script = MESSAGE_LIST_PATTERN.sub(message_list_replacer, script)
        _SENTINEL = object()
        assert next(translated_messages, _SENTINEL) is _SENTINEL

    ## Names
    script = VONAME_PATTERN.sub(name_replacer, script)

    translated_ks_file.write_text(script)
