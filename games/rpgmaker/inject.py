import json
from pathlib import Path
from gtbridge import load


original_dir = Path('./data/original_db')
translated_json_dir = Path('./data/translated_json')


def inject_list(l):
    for cmd in l:
        if cmd['code'] == 101:
            if cmd['parameters'][0]:
                message = translated.pop(0)
                assert cmd['parameters'][0] == message.original
                cmd['parameters'][0] = message.message
        elif cmd['code'] == 401:
            if cmd['parameters'][0]:
                message = translated.pop(0)
                assert cmd['parameters'][0] == message.original
                cmd['parameters'][0] = message.message
        elif cmd['code'] == 102:
            choices = cmd['parameters'][0]
            for i, s in enumerate(choices):
                if s:
                    message = translated.pop(0)
                    assert s == message.original
                    choices[i] = message.message
        elif cmd['code'] == 402:
            if cmd['parameters'][1]:
                message = translated.pop(0)
                assert cmd['parameters'][1] == message.original
                cmd['parameters'][1] = message.message


for j in translated_json_dir.rglob('*.json'):
    j_relative = j.relative_to(translated_json_dir)
    translated = load(j)
    with open(original_dir / j_relative, 'r') as f:
        db = json.load(f)

    if j.name == 'System.json':
        for key in ['basic', 'commands']:
            for i, s in enumerate(db['terms'][key]):
                if s is not None:
                    message = translated.pop(0)
                    assert s == message.original
                    db['terms'][key][i] = message.message

    elif j.name == 'Items.json':
        for item in db:
            if item and 'name' in item and item['name']:
                message = translated.pop(0)
                o_item = message.original.split('\n', 1)
                t_item = message.message.split('\n', 1)
                assert item['name'] == o_item[0]
                item['name'] = t_item[0]
                if len(t_item) > 1:
                    assert item['description'] == o_item[1]
                    item['description'] = t_item[1]

    if isinstance(db, list):
        for page in db:
            if page and 'list' in page:
                inject_list(page['list'])
            elif page and 'pages' in page:
                for subpage in page['pages']:
                    inject_list(subpage['list'])

    elif isinstance(db, dict) and 'events' in db:
        for event in db['events']:
            if event and 'pages' in event:
                for page in event['pages']:
                    if page and 'list' in page:
                        inject_list(page['list'])

    output_path = Path('./data/translated_db') / j_relative
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
