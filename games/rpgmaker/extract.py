import re
import json
from pathlib import Path
from gtbridge import MessageList

common_dict = json.loads((Path(__file__).resolve().parent / 'common.json').read_text())

data_dir = Path('./data/original_data')
json_dir = Path('./data/original_json')

MESSAGE_NAME_PATTERN = re.compile(r'%(\d)')
FREE_NAMES = [None, '梨沙', '千枝', '仁奈', '小春']


r'''
https://forums.rpgmakerweb.com/index.php?threads/a-list-for-text-commands-n-1-v-1-so-on.138500/post-1201338

\V[n] Replaced by the value of the nth variable.
\N[n] Replaced by the name of the nth actor.
\P[n] Replaced by the name of the nth party member.
\G    Replaced by the currency unit.

\C[n] Draw the subsequent text in the nth color.
\I[n] Draw the nth icon.

\{    Increases the text size by one step.
\}    Decreases the text size by one step.
\>    Display remaining text on same line all at once.
\<    Cancel the effect that displays text all at once.

\$    Opens the gold window.

\!    Waits for button input.
\^    Do not wait for input after displaying text.

\.    Waits 1/4th seconds.
\|    Waits 1 second.

\\    Replaced with the backslash character.
'''

PLACEHOLDER_PATTERN = re.compile(r'\\(.+?)(?:\[(\d+)\])?')
CONTROL_PATTERN = re.compile(r'\\[\$\{\}<>\!\^\.\|]')

def interpolation(s, actors):
    tags = []
    for match in PLACEHOLDER_PATTERN.finditer(s):
        p = match.group(0)
        tag = match.group(1).upper()
        if match.group(2):
            index = int(match.group(2))

        # index should exist for N, NN, and V
        match tag:
            case 'N':
                assert len(actors[index][0]) > 0
                s = s.replace(p, actors[index][0], 1)
            case 'NN':
                assert len(actors[index][1]) > 0
                s = s.replace(p, actors[index][1], 1)

            case 'V':
                s = s.replace(p, str(index), 1)
                tags.append(f'P:V:{index}')

            case 'G':
                s = s.replace(p, 'G', 1)

            case 'C'| 'I' | '{' | '}' | '<' | '>' | '$' | '!' | '^':
                s = s.replace(p, '', 1)
                tags.append(f'P:{tag}')

            case '.':
                s = s.replace(p, ' ', 1)
                tags.append('P:W:.')
            case '|':
                s = s.replace(p, '\n', 1)
                tags.append('P:W:|')

    if '\\' in s:
        tags.append('P:UNKNOWN')

    return (s, tags)


C356_PATTERN = re.compile(r'([\x21-\xff]+ )(.*)( [\x21-\xff]+)')

def extract_list(l, message_list, actors):
    name = ''
    for cmd in l:
        match cmd['code']:
            case 101:
                if len(cmd['parameters']) >= 5:
                    name, _ = interpolation(cmd['parameters'][4], actors)

                if cmd['parameters'][0]:
                    message_list.append(cmd['parameters'][0], name=name)
                else:
                    continue # keep name for the next messages

            case 401:
                if cmd['parameters'][0]:
                    message_list.append(cmd['parameters'][0], name=name)

            case 102:
                for s in cmd['parameters'][0]:
                    if s:
                        message_list.append(s, name='OPTION')

            case 122:
                for e in cmd['parameters']:
                    if isinstance(e, str) and e:
                        message_list.append(e, name='CAPTION')

            case 402:
                if cmd['parameters'][1]:
                    message_list.append(cmd['parameters'][1], name='OPTION')

            case 356:
                if cmd['parameters'][0]:
                    text = cmd['parameters'][0]
                    pre, text, post = C356_PATTERN.match(text).groups()
                    if pre != 'D_TEXT ':
                        continue
                    message_list.append(
                        text,
                        name='CAPTION',
                        pre=pre,
                        post=post,
                        original=cmd['parameters'][0]
                    )

            case 357:
                if isinstance(cmd['parameters'][3], dict) and 'text' in cmd['parameters'][3]:
                    message_list.append(cmd['parameters'][3]['text'], name='CAPTION')

        name = ''

def main():
    message_list = MessageList()

    for data in data_dir.rglob('data'):
        if not data.is_dir():
            continue

        actors = {}
        if (data / 'Actors.json').is_file():
            actors_data = json.loads((data / 'Actors.json').read_text())
            for actor in actors_data:
                if actor and 'id' in actor:
                    name = actor.get('name', '')
                    nickname = actor.get('nickname', '')
                    actors[actor['id']] = (name, nickname)
                    if name:
                        message_list.names[name] = 0xffff
                    if nickname:
                        message_list.names[nickname] = 0xffff

        for original_data_path in data.glob('*.json'):
            data = json.loads(original_data_path.read_text())

            if original_data_path.name == 'System.json':
                for key in ('basic', 'commands'):
                    for s in data['terms'][key]:
                        if s is not None:
                            message_list.append(s, name='OPTION')
                for _, v in data['terms']['messages'].items():
                    if v:
                        message_list.append(v, name='CAPTION')

            elif original_data_path.name == 'Enemies.json':
                for enemy in data:
                    if enemy and 'name' in enemy:
                        name, _ = interpolation(enemy['name'], actors)
                        if name:
                            message_list.names[name] = 0xffff

            elif original_data_path.name in ('Armors.json', 'Items.json', 'Weapons.json'):
                for item in data:
                    if item and 'name' in item and item['name']:
                        message_list.append(
                            f'{item["name"]}\n{item.get("description", "")}',
                            name=original_data_path.stem.upper()[:-1]
                        )

            elif original_data_path.name in ('Skills.json', 'States.json'):
                for item in data:
                    original = []
                    if item and 'name' in item and item['name']:
                        for field in ('name', 'description', 'message1', 'message2', 'message3', 'message4'):
                            if field in item and item[field]:
                                assert '\n\n' not in item[field]
                                original.append(item[field])
                        original = '\n\n'.join(original)

                        text = original
                        tags = []
                        for match in MESSAGE_NAME_PATTERN.finditer(original):
                            p = match.group(0)
                            index = int(match.group(1))
                            text = text.replace(p, FREE_NAMES[index], 1)
                            tags.append(p)

                        message_list.append(text, original=original, name=original_data_path.stem.upper()[:-1], tags=tags)


            elif isinstance(data, list):
                for page in data:
                    if page and 'list' in page:
                        extract_list(page['list'], message_list, actors)
                    elif page and 'pages' in page:
                        for subpage in page['pages']:
                            extract_list(subpage['list'], message_list, actors)

            elif isinstance(data, dict) and 'events' in data:
                for event in data['events']:
                    if event and 'pages' in event:
                        for page in event['pages']:
                            if page and 'list' in page:
                                extract_list(page['list'], message_list, actors)


            for message in message_list.messages:
                if message.pre and message.pre[-1] == '\\':
                    message.pre = message.pre[:-1]
                    message.message = '\\' + message.message

                while CONTROL_PATTERN.match(message.message[:2]):
                    message.pre += message.message[:2]
                    message.message = message.message[2:]

                while CONTROL_PATTERN.match(message.message[-2:]):
                    message.post = message.message[-2:] + message.post
                    message.message = message.message[:-2]

                message.message, _tags = interpolation(message.message, actors)
                message.tags += _tags

                if (
                    message.name in ('CAPTION', 'OPTION', 'ARMOR', 'ITEM', 'SKILL', 'STATE')
                    and message.original in common_dict
                ):
                    message.pre = common_dict[message.original]
                    message.message = ''
                    message.tags.clear()

            original_json_path = json_dir / original_data_path.relative_to(data_dir)
            original_json_path.parent.mkdir(parents=True, exist_ok=True)
            message_list.flush(original_json_path)

    message_list.dump_stats('./names.json')


if __name__ == '__main__':
    main()
