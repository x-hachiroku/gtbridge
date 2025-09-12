import json
from pathlib import Path
from gtbridge import MessageList

strs = {}
raw_dir = Path('./data/raw')

def parse_list(strs, l):
    for cmd in l:
        if cmd['code'] in {101, 401}:
            strs[cmd['parameters'][0]] = None
        elif cmd['code'] == 102:
            for s in cmd['parameters'][0]:
                strs[s] = None
        elif cmd['code'] == 402:
            strs[cmd['parameters'][1]] = None


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
    message_list.append(s)

message_list.flush('./data/original.json')
message_list.dump_stats()
