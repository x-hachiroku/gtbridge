import os

from message import MessageList
from patterns import *

if not os.path.isdir('./data/original_json'):
    os.mkdir('./data/original_json')

class PRMessageList(MessageList):
    def preprocess(self, text, tags):
        for match in FURIGANA_PATTERN.finditer(text):
            if match.group(2) in VALID_FURIGANAS:
                tags.append('furigana')
                text = text.replace(
                    f'<ruby {match.group(1)},{match.group(2)}>{match.group(1)}',
                    f' {match.group(1)}({match.group(2)}) '
                )
            else:
                print(f'{blob} skipping furigana: {match.group(1)}({match.group(2)})')
                text = text.replace(
                    f'<ruby {match.group(1)},{match.group(2)}>{match.group(1)}',
                    match.group(1)
                )

        return super().preprocess(text, tags)


message_list = PRMessageList()
for blob in os.listdir('./data/original_blob'):
    if blob == 'select':
        continue

    s = Script(blob)
    if len(s.texts) == 0:
        print(f'{blob}: no texts found')
        continue

    message_list.append(s.title, name='タイトル')

    for match in MESSAGE_PATTERN.finditer(s.instructions_bytes):
        name =  s.get_text(match.group(2)) if match.group(2) else ''
        text = s.get_text(match.group(1))
        original = text
        message_list.append(text, name=name, original=original)

    for alias_index in ALIAS_PATTERN.findall(s.instructions_bytes):
        alias = s.get_text(alias_index)
        if alias not in message_list.names:
            message_list.names[alias] = 0

    s.check_used()
    message_list.flush(f'./data/original_json/{blob}.json')


with open('./data/original_blob/select', 'rb') as f:
    data = f.read()[0x5ecb:]
    for option_bytes in data.split(b'\x00')[:-1]:
        option = option_bytes.decode('cp932')
        message_list.append(option, name='選択肢')
    message_list.flush('./data/original_json/select.json')


message_list.dump_stats('./names.json')
