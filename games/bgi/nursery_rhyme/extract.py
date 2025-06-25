import os

from message import MessageList
from patterns import *

if not os.path.isdir('./data/original_json'):
    os.mkdir('./data/original_json')

message_list = MessageList()
for blob in os.listdir('./data/original_blob'):
    with open(f'./data/original_blob/{blob}', 'rb') as f:
        data = f.read()

    for groups in OPTIONS_PATTERN.findall(data):
        options_num = int.from_bytes(groups[0], 'little')
        options = groups[1].split(b'\x00')
        assert len(options) == options_num, \
                f'{blob}: {len(options)} options found, {options_num} expected.'

        for option in options:
            option_text = option.decode('cp932')
            message_list.append(option_text, name='選択肢')


    if messages := MESSAGE_PATTERN.findall(data):
        text_count = data[int.from_bytes(messages[0][1], 'little'):].count(b'\x00')
        assert text_count == len(messages), f'{text_count} found, {len(messages)} expected.'

        for message in messages:
            start = int.from_bytes(message[1], 'little')
            end = data.find(b'\x00', start)
            text = data[start:end].decode('cp932')
            name = message[0].decode('cp932')
            message_list.append(text, name=name)

    count = message_list.flush(f'./data/original_json/{blob}.json')
    if count == 0:
        print(f'{blob}: No message found.')

message_list.dump_stats('./names.json')
