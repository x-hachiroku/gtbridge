import re
from pathlib import Path

from gtbridge import MessageList

MESSAGE_PATTERN = re.compile(
    r'(\[tb_start_text mode=[^\]]+\]\s*(?:\[[^\]]*\]\s*)*'
    r'(?:#(.*?)\s+)?)'
    r'(.*?)'
    r'((?:\[[^\]]*\])*\s*\[_tb_end_text\])',
    re.DOTALL
)

MESSAGE_LIST_PATTERN = re.compile(r'\[eval exp="f.lines = \[(.*?)\]\[f.random_num.? - 1\]"\]')

original_json_dir = Path('./data/original_json')
original_json_dir.mkdir(parents=True, exist_ok=True)

message_list = MessageList()

scenario_dir = Path('./data/app/data/scenario')

for ks in scenario_dir.rglob('*.ks'):
    ks_relative = original_json_dir / ks.relative_to(scenario_dir)
    ks_relative.parent.mkdir(parents=True, exist_ok=True)

    with open(ks, 'r') as f:
        data = f.read()

    for match in MESSAGE_PATTERN.finditer(data):
        text = match.group(3)
        text = text.replace('[r]', '')
        text = text.replace('\n', '')

        message_list.append(
            original = match.group(0),
            pre = match.group(1),
            name = match.group(2) or '',
            text = text,
            post = match.group(4),
        )

    count = message_list.flush(str(ks_relative) + '.json')

    i = 0
    for match in MESSAGE_LIST_PATTERN.finditer(data):
        messages = match.group(1).split(', ')
        for message in messages:
            message = message.strip("'")
            message_list.append(message, name='')

        count += message_list.flush(f'{ks_relative}.extra{i:02d}.json')
        i += 1

    if count == 0:
        print(f'{ks}: No message found.')

message_list.dump_stats('./names.json')
