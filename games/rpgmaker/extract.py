import re
import json
from pathlib import Path
from gtbridge import MessageList


options_path = Path(__file__).resolve().parent / 'options.json'
cwd_opts = Path('options.json')
if options_path.exists():
    with open(options_path, 'r') as f:
        options = json.load(f)
else:
    options = {}

original_dir = Path('./data/original_db')
original_json_dir = Path('./data/original_json')


def extract_list(l):
    name = ''
    for cmd in l:
        if cmd['code'] == 101:
            if len(cmd['parameters']) >= 5:
                   name = cmd['parameters'][4].strip()
            if cmd['parameters'][0]:
                message_list.append(cmd['parameters'][0], name=name)
        elif cmd['code'] == 401:
            if cmd['parameters'][0]:
                message_list.append(cmd['parameters'][0], name=name)
            name = ''
        elif cmd['code'] == 102:
            name = ''
            for s in cmd['parameters'][0]:
                if s:
                    message_list.append(s, name='OPTION')
        elif cmd['code'] == 402:
            name = ''
            if cmd['parameters'][1]:
                message_list.append(cmd['parameters'][1], name='OPTION')


message_list = MessageList()

for j in original_dir.rglob('*.json'):
    j_relative = j.relative_to(original_dir)
    with open(j, 'r') as f:
        db = json.load(f)

    if j.name == 'System.json':
        for key in ['basic', 'commands']:
            for s in db['terms'][key]:
                if s is not None:
                    message_list.append(s, name='OPTION')

    elif j.name == 'Items.json':
        for item in db:
            if item and 'name' in item and item['name']:
                message_list.append(f'{item["name"]}\n{item.get("description", "")}', name='ITEM')

    elif isinstance(db, list):
        for page in db:
            if page and 'list' in page:
                extract_list(page['list'])
            elif page and 'pages' in page:
                for subpage in page['pages']:
                    extract_list(subpage['list'])

    elif isinstance(db, dict) and 'events' in db:
        for event in db['events']:
            if event and 'pages' in event:
                for page in event['pages']:
                    if page and 'list' in page:
                        extract_list(page['list'])


    for message in message_list.messages:
        if '\\' in message.message:
             message.tags.append('ESCAPE')
        if message.name == 'OPTION' and message.message in options:
            message.pre = options[message.message]
            message.message = ''

    (original_json_dir / j_relative).parent.mkdir(parents=True, exist_ok=True)
    message_list.flush(original_json_dir / j_relative)

message_list.dump_stats('./names.json')
