import re
from pathlib import Path

from gtbridge import MessageList

SCRIPT_START_PATTERN = re.compile(r'\[\s*iscript')
SCRIPT_END_PATTERN = re.compile(r'\[\s*endscript')
HTML_START_PATTERN = re.compile(r'\[\s*html')
HTML_END_PATTERN = re.compile(r'\[\s*endhtml')

NAME_PATTERN = re.compile(r'\[setname.* name=(.*?)\s*\]')
MSG_PATTERN = re.compile(r'^(.*?)\s*(\[.*\])?$')

scenario_dir = Path('./data/scenario')
original_json_dir = Path('./data/original_json')
original_json_dir.mkdir(parents=True, exist_ok=True)

message_list = MessageList()

for ks in scenario_dir.rglob('*.ks'):
    print(ks)
    ks_relative = original_json_dir / ks.relative_to(scenario_dir)
    ks_relative.parent.mkdir(parents=True, exist_ok=True)

    with open(ks, 'r') as f:
            lines = f.read().splitlines()

    i = 0
    name = ''
    while i < len(lines):
        line = lines[i].strip()

        if SCRIPT_START_PATTERN.match(line):
            while not SCRIPT_END_PATTERN.search(lines[i]):
                i += 1

        elif HTML_START_PATTERN.match(line):
            while not HTML_END_PATTERN.search(lines[i]) :
                i += 1

        elif match := NAME_PATTERN.match(line):
            name = match.group(1).strip()

        elif not line.strip() or line[0] in {';', '*', '['}:
            pass

        else:
            match = MSG_PATTERN.match(line)
            msg = match.group(1).strip()
            msg = msg.replace('[r]', '').replace('[l]', '')
            post = match.group(2)
            message_list.append(
                msg,
                name=name,
                original=line,
                pre='',
                post=post.strip() if post else '',
                tags=[i]
            )
            name = ''

        i += 1


    count = message_list.flush(str(ks_relative) + '.json')
    if count == 0:
        print(f'{ks}: No message found.')

message_list.dump_stats('./names.json')
