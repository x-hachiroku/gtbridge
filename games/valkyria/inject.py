import os
import re
import json
from glob import glob
from pathlib import Path


if not os.path.exists('./data/translated_scripts'):
    os.makedirs('./data/translated_scripts')
    os.makedirs('./data/translated_scripts/data02')
    os.makedirs('./data/translated_scripts/data03')


def write(s, script):
    script = re.sub('♪', '＃', script)
    script = re.sub('・', '·', script)
    with open(f'./data/translated_scripts/{s}', 'w', encoding='cp936') as f:
        f.write(script)


def load(j):
    def to_fullwidth(s):
        res = []
        for c in s:
            if ' ' < c <= '~':
                res.append(chr(ord(c) + 0xFEE0))
            elif c != ' ':
                res.append(c)
        res = ''.join(res)
        return res

    with open(j, 'r') as f:
        translated_messages = json.load(f)

    for m in translated_messages:
        if len(m['message']) > 0:
            if m['message'][-1] == '。':
                m['message'] = m['message'][:-1]
            if m['message'][0] == '「' and m['message'][-1] == '」':
                m['message'] = m['message'][1:-1]
        m['message'] = to_fullwidth(m['message'])
        m['message'] = m['pre'] + m['message'] + m['post']
        if 'option' in m['tags']:
            m['message'] = m['message'].replace('\n', '", "')
    return translated_messages


for s in glob('data/original_scripts/**/*', recursive=True):
    if os.path.isdir(s):
        continue

    basename = '/'.join(s.split('/')[2:])

    with open(s, 'r', encoding='cp932') as f:
        script = f.read()

    if not os.path.exists(f'./data/translated_json/{basename}.json'):
        print(f'{s}: no translation found, skipping')
        write(basename, script)
        continue

    translated_messages = load(f'./data/translated_json/{basename}.json')
    for translated_message in translated_messages:
        assert translated_message['original'] in script, \
            f'Original message not found in {s}: {translated_message.original}'
        translated_message['message'] = translated_message['message'].replace('\n', '", "')
        script = script.replace(translated_message['original'], translated_message['message'], 1)

    write(basename, script)
