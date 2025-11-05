import re
import json
from shutil import copy
from pathlib import Path
from gtbridge import MessageList, load

TAG_PATTERN = re.compile(r'\A<.*?>', re.DOTALL)
PRE_ESCAPE_PATTERN = re.compile(r'\A\\[A-Za-z]+\[\d+\]', re.DOTALL)
POST_ESCAPE_PATTERN = re.compile(r'\\[A-Za-z]+\[\d+\]\s*\Z', re.DOTALL)
RUBY_PATTERN = re.compile(r'\\r\[(.*?),(.*?)\]', re.DOTALL)

DATA_DIRS = (
    'BGM/',
    'BasicData/',
    'CharaChip/',
    'CharacterGraphic/',
    'MapChip/',
    'MapData/',
    'Picture/',
    'SE/',
    'SystemGraphic/',
)

names_path = Path('./names.json')
if names_path.exists():
    NAMES = json.loads(names_path.read_text())
else:
    NAMES = {}


def walk_page_list(page_list, extract, message_list):
    if extract:
        def handle_text(op, name, message_list):
            message_list.append(
                op['stringArgs'][0].replace('\r\n', '\n'),
                name=name,
                original=op['stringArgs'][0]
            )

        def handle_message(op, message_list):
            pre = ''
            post = ''
            tags = []

            message = op['stringArgs'][1]
            if message[0] == '＠':
                name, message = message[1:].split('\r\n', 1)
            elif len(op['stringArgs']) >= 3 and op['stringArgs'][2]:
                name = op['stringArgs'][2]
            else:
                name = ''
            message = message.replace('\r\n', '\n')

            if match := TAG_PATTERN.match(message):
                pre = match.group()
                message = message[len(pre):]

            for match in RUBY_PATTERN.finditer(message):
                base, ruby = match.groups()
                message = message.replace(match.group(0), base, 1)
                tags.append('RUBY')

            if match := PRE_ESCAPE_PATTERN.match(message):
                pre += match.group()
                message = message[len(match.group()):]

            if match := POST_ESCAPE_PATTERN.search(message):
                post = match.group() + post
                message = message[:match.start()]

            if '\\' in message:
                tags.append('ESCAPE')

            message_list.append(
                message,
                name=name,
                original=op['stringArgs'][1],
                pre=pre,
                post=post,
                tags=tags
            )

        def handle_option(op, message_list):
            for choice in op['stringArgs'][1:]:
                assert '\n' not in choice
            message = '\n'.join(op['stringArgs'][1:])
            message_list.append(message, name='OPTION')

    else:
        def handle_text(op, name, message_iter):
            message = next(message_iter)
            assert message.original == op['stringArgs'][0]
            op['stringArgs'][0] = message.message.replace('\n', '\r\n')

        def handle_message(op, message_iter):
            message = next(message_iter)

            text = message.message.replace('\n', '\r\n')
            if message.original[0] == '＠':
                text = f'＠{NAMES[message.name]}\n{text}'
            elif message.name:
                op['stringArgs'][2] = NAMES[message.name]

            op['stringArgs'][1] = text

        def handle_option(op, message_iter):
            message = next(message_iter)
            choices = message.message.split('\n')
            assert len(choices) == len(op['stringArgs']) - 1
            for i in range(len(choices)):
                op['stringArgs'][i+1] = choices[i]

    i = 0
    while i < len(page_list):
        op = page_list[i]
        i += 1

        if len(op.get('stringArgs', [])) == 0:
            continue

        if op['code'] == 101:
            handle_text(op, '', message_list)
            continue

        if op['code'] == 122:
            if i < len(page_list) and page_list[i]['code'] in (210, 250, 300):
                if op['stringArgs'][0].startswith(DATA_DIRS):
                    continue
                if (
                    page_list[i]['code'] == 210
                    and len(page_list[i].get('stringArgs', [])) > 2
                ):
                    assert page_list[i]['stringArgs'][1] == ''
                    name = page_list[i]['stringArgs'][2]
                    page_list[i]['stringArgs'][2] = NAMES.get(name, name) # Does nothing when extracting
                else:
                    name = ''

                handle_text(op, name, message_list)

                i += 1
            continue


        # Handle 210 and 300
        if len(op.get('stringArgs', [])) < 2 or not op['stringArgs'][1]:
            continue

        if op['code'] == 210:
            if op['intArgs'][0] == 500013:
                handle_option(op, message_list)
                continue

            if not op['intArgs'][0] in (500004, 500005, 500006, 500018):
                print(f'Unknown code 210 arg: {op}')
                continue

        elif op['code'] == 300:
            if op.get('stringArgs', [''])[0] == '選択肢':
                handle_option(op, message_list)
                continue

            if not op['intArgs'][1] in (4112, 4113, 4114, 4115, 12372, 28756, 110676, 16781330):
                print(f'Unknown code 300 arg: {op}')
                continue

        else:
            continue

        if not op['stringArgs'][1]:
            continue

        handle_message(op, message_list)


def handle_wolf(extract):
    if extract:
        json_dir = Path('./data/original_json')
        message_list = MessageList()
    else:
        json_dir = Path('./data/translated_json')

    original_data_dir = Path('./data/original_data')
    translated_data_dir = Path('./data/translated_data')

    for original_data_path in (original_data_dir).rglob('*.json'):
        relative_path = original_data_path.relative_to(original_data_dir)
        json_path = json_dir/relative_path
        translated_data_path = translated_data_dir/relative_path
        json_path.parent.mkdir(parents=True, exist_ok=True)
        translated_data_path.parent.mkdir(parents=True, exist_ok=True)

        if not extract:
            if not json_path.exists():
                copy(original_data_path, translated_data_path)
                continue
            message_list = iter(load(json_path))

        data = json.loads(original_data_path.read_text())

        if original_data_path.parts[-2] == 'mps':
            for e in data['events']:
                for p in e['pages']:
                    walk_page_list(p['list'], extract, message_list)
        elif original_data_path.parts[-2] == 'common':
            walk_page_list(data['commands'], extract, message_list)

        if extract:
            message_list.flush(json_path)
        else:
            translated_data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    if extract:
        message_list.dump_stats('./names.json')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['e', 'i'])

    if parser.parse_args().mode == 'e':
        handle_wolf(extract=True)
    else:
        handle_wolf(extract=False)
