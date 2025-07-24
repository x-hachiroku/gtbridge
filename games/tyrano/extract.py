import re
import os

from message import MessageList

MESSAGE_PATTERN = re.compile(
    r'(\[tb_start_text mode=1 \]\n*' + r'#(.*?)\n+)' +
    r'(.*?)' +
    r'((?:\[p\])?\n*\[_tb_end_text\])',
    re.DOTALL
)

MESSAGE_LIST_PATTERN = re.compile(r'\[eval exp="f.lines = \[(.*?)\]\[f.random_num.? - 1\]"\]')

if not os.path.isdir('./data/original_json'):
    os.mkdir('./data/original_json')

message_list = MessageList()

for ks in os.listdir('./data/app/data/scenario'):
    if not ks.endswith('.ks'):
        continue
    with open(f'./data/app/data/scenario/{ks}', 'r') as f:
        data = f.read()

    for match in MESSAGE_PATTERN.finditer(data):
        message_list.append(
            pre = match.group(1),
            name = match.group(2),
            text = match.group(3),
            post = match.group(4),
        )

    count = message_list.flush(f'./data/original_json/{ks}.json')

    i = 0
    for match in MESSAGE_LIST_PATTERN.finditer(data):
        messages = match.group(1).split(', ')
        for message in messages:
            message = message.strip("'")
            message_list.append(message, name='')

        count += message_list.flush(f'./data/original_json/{ks}.extra{i:02d}.json')
        i += 1

    if count == 0:
        print(f'{ks}: No message found.')

message_list.dump_stats('./names.json')
