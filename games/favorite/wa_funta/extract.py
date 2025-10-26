import re
from pathlib import Path
from gtbridge import MessageList

RUBY_PATTERN = re.compile( r'\[(.*?)\|(.*?)\]', re.DOTALL)

message_list = MessageList()

for txt in Path('./data/original_txt').glob('*.txt'):
    with open(txt, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    extracted_lines = []
    name = ''
    for line in lines:
        if not line.strip() or '_' in line or '/' in line:
            continue

        if line[0] == '【' and line[-1] == '】':
            name = line[1:-1]
            continue

        pre = ''
        post = ''
        tags = []
        original = line
        while line and line[0] == '<':
            pre += line[:3]
            line = line[3:]
        while line and line[-1] == '>':
            post = line[-3:] + post
            line = line[:-3]

        if '<' in line:
            tags.append('MOJI')

        for match in RUBY_PATTERN.finditer(line):
            full_match = match.group(0)
            ruby_text = match.group(1)
            base_text = match.group(2)
            line = line.replace(full_match, base_text)
            tags.append(f'RUBY:{full_match}')

        message_list.append(line,
            original=original,
            name=name,
            pre=pre,
            post=post,
            tags=tags
        )
        name = ''

message_list.flush('./data/original_json/messages.json')
message_list.dump_stats()
