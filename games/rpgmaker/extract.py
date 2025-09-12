import re
import json
from pathlib import Path
from gtbridge import MessageList

_ESCAPE_PATTERN = r'(\\.*?\[.*?\]+)'
ESCAPE_AT_START_PATTERN = re.compile(r'^' + _ESCAPE_PATTERN + r'(.*)$')
ESCAPE_AT_END_PATTERN = re.compile(r'^(.*)' + _ESCAPE_PATTERN + r'$')

strs = {}
raw_dir = Path('./data/raw')

def parse_list(strs, l):
    name = ''
    for cmd in l:
        if cmd['code'] == 101:
            if len(cmd['parameters']) >= 5:
                   name = cmd['parameters'][4].strip()
            strs[cmd['parameters'][0]] = name
        elif cmd['code'] == 401:
            strs[cmd['parameters'][0]] = name
            name = ''
        elif cmd['code'] == 102:
            for s in cmd['parameters'][0]:
                strs[s] = 'BUTTON'
            name = ''
        elif cmd['code'] == 402:
            strs[cmd['parameters'][1]] = 'BUTTON'
            name = ''


for j in raw_dir.rglob('*.json'):
    with open(j, 'r') as f:
        db = json.load(f)

    if isinstance(db, list):
        for page in db:
            if page and 'list' in page:
                parse_list(strs, page['list'])

    elif isinstance(db, dict) and 'events' in db:
        for event in db['events']:
            if event and 'pages' in event:
                for page in event['pages']:
                    if page and 'list' in page:
                        parse_list(strs, page['list'])

message_list = MessageList()
for s in strs:
    assert type(s) is str, s

    pre = ''
    post = ''
    name = strs[s]
    tags = []
    if not name:
        name = None

    message_list.append(s,
        name=name,
        pre=pre,
        post=post,
        tags=tags
    )

for message in message_list.messages:
    if match := ESCAPE_AT_START_PATTERN.match(message.message):
        message.pre = message.pre + match.group(1)
        message.message = match.group(2)
    if match := ESCAPE_AT_END_PATTERN.match(message.message):
        message.message = match.group(1)
        message.post = match.group(2) + message.post
    if '\\' in message.message:
         message.tags.append('ESCAPE')

message_list.flush('./data/original.json')
message_list.dump_stats('./names.json')
