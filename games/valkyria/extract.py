import os
import re
import json
from glob import glob
from gtbridge import MessageList


if not os.path.exists('./data/original_json'):
    os.mkdir('./data/original_json')
    os.mkdir('./data/original_json/data02')
    os.mkdir('./data/original_json/data03')

NAME_PATTERN = re.compile(
    r'%SetNameWindow\(\s*(\d+)\s*,.*?\)'
)

# CTRL_SEQ_PATTERN = re.compile(r'/[0-9a-zA-Z]')
CTRL_SEQ_PATTERN = re.compile(r'/r')

MESSAGE_PATTERN = re.compile(
    r'%SetMessage\(\s*"(?:/[0-9a-zA-Z])?(.*)",.*?\)'
)

OPTION_PATTERN = re.compile(
    r'%SetSelectEx\(\s*"((.*)",\s*"(.*))",.*?\)'
)


message_list = MessageList()

with open('./namelist.json', 'r') as f:
    namelist = json.load(f)

for s in glob('data/original_scripts/**/*', recursive=True):
    if os.path.isdir(s):
        continue

    basename = '/'.join(s.split('/')[2:])
    with open(s, 'r', encoding='cp932') as f:
        script = f.readlines()

    name = ''
    for line in script:
        if NAME_PATTERN.match(line):
            name = namelist[int(NAME_PATTERN.match(line).group(1))]

        elif MESSAGE_PATTERN.match(line):
            match = MESSAGE_PATTERN.match(line)
            original = match.group(0)
            message = match.group(1)
            pre, post = original.split(message)
            message = CTRL_SEQ_PATTERN.sub('', message).strip()
            message_list.append(message, name=name, pre=pre, post=post, original=original)

        elif OPTION_PATTERN.match(line):
            match = OPTION_PATTERN.match(line)
            original = match.group(0)
            message = match.group(2) + '\n' + match.group(3)
            pre, post = original.split(match.group(1))
            message_list.append(message, name='選択肢', pre=pre, post=post, original=original, tags=['option'])

    count = message_list.flush(f'./data/original_json/{basename}.json')
    if count == 0:
        print(f'{s}: No message found.')

message_list.dump_stats()
