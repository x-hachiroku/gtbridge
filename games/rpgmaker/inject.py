import re
import json
from shutil import copyfile
from pathlib import Path

from gtbridge import load
from extract import FREE_NAMES, PLACEHOLDER_PATTERN, NAME_PATTERN

LABEL_PATTERN = re.compile(r'<[^>]*>')
EXP_PATTERN = re.compile(r'[a-z]+\(.*?\)')

origina_data_dir = Path('./data/original_data')
translated_json_dir = Path('./data/translated_json')
translated_data_dir = Path('./data/translated_data')

names_path = Path('./names.json')
if names_path.is_file():
    names = json.loads(names_path.read_text())
    names = sorted(names.items(), key=lambda x: -len(x[0]))
    names = {k: v for k, v in names if k}
else:
    print('Warning: names.json not found.')
    names = {}


def inject_list(l, translated):
    for cmd in l:
        match cmd['code']:
            case 101:
                if len(cmd['parameters']) >= 5:
                    cmd['parameters'][4] = names.get(cmd['parameters'][4], cmd['parameters'][4])

                if cmd['parameters'][0]:
                    message = next(translated)
                    assert cmd['parameters'][0] == message.original
                    cmd['parameters'][0] = message.message

            case 401:
                if cmd['parameters'][0]:
                    if NAME_PATTERN.match(cmd['parameters'][0]):
                        for name in names:
                            cmd['parameters'][0] = cmd['parameters'][0].replace(name, names[name])
                    else:
                        message = next(translated)
                        assert cmd['parameters'][0] == message.original, (cmd['parameters'][0], message.original)
                        cmd['parameters'][0] = message.message

            case 102:
                choices = cmd['parameters'][0]
                for i, s in enumerate(choices):
                    if s:
                        message = next(translated)
                        assert s == message.original
                        choices[i] = message.message

            case 122:
                for i, e in enumerate(cmd['parameters']):
                    if isinstance(e, str) and e:
                        message = next(translated)
                        assert e == message.original
                        cmd['parameters'][i] = message.message


            case 402:
                if cmd['parameters'][1]:
                    message = next(translated)
                    assert cmd['parameters'][1] == message.original
                    cmd['parameters'][1] = message.message

            case 356:
                if cmd['parameters'][0]:
                    if cmd['parameters'][0].split(' ')[0] not in ('D_TEXT', 'ShowInfo'):
                        continue
                    message = next(translated)
                    assert cmd['parameters'][0] == message.original
                    cmd['parameters'][0] = message.message

            case 357:
                if isinstance(cmd['parameters'][3], dict) and 'text' in cmd['parameters'][3]:
                    message = next(translated)
                    assert cmd['parameters'][3]['text'] == message.original
                    cmd['parameters'][3]['text'] = message.message


def main():
    for original_data_path in origina_data_dir.rglob('*.json'):
        translated_data_path = translated_data_dir / original_data_path.relative_to(origina_data_dir)
        translated_data_path.parent.mkdir(parents=True, exist_ok=True)
        data = json.loads(original_data_path.read_text(encoding='utf-8-sig'))

        if original_data_path.name in ('Actors.json', 'Enemies.json'):
            for actor in data:
                if not actor:
                    continue
                if 'name' in actor and actor['name']:
                    actor['name'] = names.get(actor['name'], actor['name'])
                if 'nickname' in actor and actor['nickname']:
                    actor['nickname'] = names.get(actor['nickname'], actor['nickname'])

            translated_data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
            continue

        translated_json_path = translated_json_dir / original_data_path.relative_to(origina_data_dir)
        if not translated_json_path.is_file():
            copyfile(original_data_path, translated_data_path)
            continue

        translated = load(translated_json_path)

        for message in translated:
            tags = {}
            for tag in message.tags:
                if tag not in tags:
                    tags[tag] = 0
                tags[tag] += 1

            for tag in list(tags.keys()):
                count = tags[tag]

                match tag:
                    case 'P:W:.':
                        assert count == message.message.count(' '), message.original
                        message.message = message.message.replace(' ', '\\.')

                    case 'P:W:|':
                        assert count == message.message.count('\n'), message.original
                        message.message = message.message.replace('\n', '\\|')

                    case x if x.startswith('P:V:'):
                        index = tag[4:]
                        assert count == message.message.count(index), message.original
                        message.message = message.message.replace(index, f'\\V[{index}]')

                    case x if x.startswith('%'):
                        index = int(tag[1:])
                        assert count == message.message.count(FREE_NAMES[index]), message.original
                        message.message = message.message.replace(FREE_NAMES[index], tag)

            # assert message.original.upper().count('\\V') == message.message.count('\\V'), message.original
            for match in PLACEHOLDER_PATTERN.finditer(message.original):
                placeholder = match.group(0)
                assert message.original.upper().count(placeholder) == message.message.upper().count(placeholder), (message.original, message.message)
            for match in LABEL_PATTERN.finditer(message.original):
                label = match.group(0)
                assert message.original.count(label) == message.message.count(label) or ('SG説明' in message.message and 'SG説明' in label), (message.original, message.message)
            for match in EXP_PATTERN.finditer(message.original):
                if message.original.count(match.group(0)) != message.message.count(match.group(0)):
                    print('Warning: EXP function count mismatch:', message.original, message.message)

        translated = iter(translated)

        if original_data_path.name == 'System.json':
            if 'currencyUnit' in data:
                message = next(translated)
                assert data['currencyUnit'] == message.original, (data['currencyUnit'], message.original)
                data['currencyUnit'] = message.message

            for key in ('elements', 'equipTypes', 'skillTypes'):
                for i, s in enumerate(data[key]):
                    if s is not None:
                        message = next(translated)
                        assert s == message.original, (s, message.original)
                        data[key][i] = message.message

            for key in ('basic', 'commands'):
                for i, s in enumerate(data['terms'][key]):
                    if s is not None:
                        message = next(translated)
                        assert s == message.original
                        data['terms'][key][i] = message.message

            for k, v in data['terms']['messages'].items():
                if v:
                    message = next(translated)
                    assert v == message.original, (v, message.original)
                    data['terms']['messages'][k] = message.message

        elif original_data_path.name in ('Armors.json', 'Items.json', 'Weapons.json'):
            for item in data:
                if item and 'name' in item and item['name']:
                    message = next(translated)
                    o_item_l = message.original.split('\n', 1)
                    t_item_l = message.message.split('\n', 1)
                    assert item['name'] == o_item_l[0]
                    item['name'] = t_item_l[0]
                    assert item['description'] == o_item_l[1]
                    item['description'] = t_item_l[1]
                    if note := item.get('note', ''):
                        message = next(translated)
                        assert note == message.original
                        item['note'] = message.message

        elif original_data_path.name in ('Skills.json', 'States.json'):
            for item in data:
                if item and 'name' in item and item['name']:
                    message = next(translated)
                    o_skill_list = message.original.split('\n\n')
                    t_skill_list = message.message.split('\n\n')
                    assert len(o_skill_list) == len(t_skill_list), (message.original, message.message)
                    o_skill_iter = iter(o_skill_list)
                    t_skill_iter = iter(t_skill_list)
                    for field in ('name', 'description', 'message1', 'message2', 'message3', 'message4'):
                        if field in item and item[field]:
                            assert next(o_skill_iter) == item[field]
                            item[field] = next(t_skill_iter)
                    _SENTINEL = object()
                    assert next(o_skill_iter, _SENTINEL) is _SENTINEL

        if isinstance(data, list):
            for page in data:
                if page and 'list' in page:
                    inject_list(page['list'], translated)
                elif page and 'pages' in page:
                    for subpage in page['pages']:
                        inject_list(subpage['list'], translated)

        elif isinstance(data, dict) and 'events' in data:
            for event in data['events']:
                if event and 'pages' in event:
                    for page in event['pages']:
                        if page and 'list' in page:
                            inject_list(page['list'], translated)

        _SENTINEL = object()
        assert next(translated, _SENTINEL) is _SENTINEL

        translated_data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
