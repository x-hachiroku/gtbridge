import os
import json

from patterns import *
from message import load


def name_replacer(match):
    if match.group(1):
        name = names_table_encoded[match.group(1)]
        delta = len(name) - len(match.group(1))
        for i in goto_addrs:
            if goto_addrs[i][0] > match.start():
                goto_addrs[i][1] += delta
        return match.group(0).replace(match.group(1), name)

    else:
        return match.group(0)


def options_replacer(match):
    count = int.from_bytes(match.group(1), 'little')
    translated_options = translated_messages[:count]
    del translated_messages[:count]

    original_options = [x.decode('cp932') for x in match.group(2).split(b'\x00')]
    assert count == len(original_options), \
            f'{blob}: {len(original_options)} options found, {count} expected.'
    for i in range(count):
        assert translated_options[i].original == original_options[i], \
                f'{blob}: Option mismatch: {translated_options[i].original} and {original_options[i]}'

    translated_options = [x.message.encode('cp936') for x in translated_options]
    translated_options_bytes = b'\x00'.join(translated_options)

    delta = len(translated_options_bytes) - len(match.group(2))
    for i in goto_addrs:
        if goto_addrs[i][0] > match.start():
            goto_addrs[i][1] += delta

    return match.group(0).replace(match.group(2), translated_options_bytes)


def goto_replacer(match):
    count = len(match.groups())
    replacement = match.group(0)[:-count * 4]
    for i in match.groups():
        replacement += goto_addrs[int.from_bytes(i, 'little')][1].to_bytes(4, 'little')
    return replacement


if not os.path.isdir('./data/translated_blob'):
    os.mkdir('./data/translated_blob')


with open('./names.json', 'r') as f:
    _names_table = json.load(f)
names_table_encoded = { k.encode('cp932') : v.encode('cp936') for k, v in _names_table.items() }

with open('./data/original_blob/font', 'rb') as f:
    font_blob = f.read()

for name in names_table_encoded:
    font_blob = font_blob.replace(name, names_table_encoded[name])

with open('./data/translated_blob/font', 'wb') as f:
    f.write(font_blob)


for blob in os.listdir('./data/original_blob'):
    if not os.path.exists(f'./data/translated_json/{blob}.json'):
        print(f'{blob}: No translation found.')
        continue

    with open(f'./data/original_blob/{blob}', 'rb') as f:
        data = f.read()
    translated_messages = load(f'./data/translated_json/{blob}.json')
    for message in translated_messages:
        assert len(message.message) < 255, f'{blob}: Message "{message.message}" too long.'

    original_messages = []
    if message_match := MESSAGE_PATTERN.search(data):
        text_start = int.from_bytes(message_match.group(2), 'little')
        original_messages = [x.decode('cp932') for x in data[text_start:].split(b'\x00')][:-1]
        data = data[:text_start]

    # Track all goto indexes
    goto_addrs = {}
    for pattern in JUMP_PATTERNS:
        for match in pattern.finditer(data):
            for group in match.groups():
                _goto_addrs = int.from_bytes(group, 'little')
                goto_addrs[_goto_addrs] = [_goto_addrs, _goto_addrs]

    # Replace name and options
    data = MESSAGE_PATTERN.sub(name_replacer, data)
    goto_addrs = { k : [v[1], v[1]] for k, v in goto_addrs.items() }
    data = OPTIONS_PATTERN.sub(options_replacer, data)

    assert len(original_messages) == len(translated_messages), \
            f'{blob}: {len(original_messages)} original messages found, {len(translated_messages)} translated_messages.'

    # Update goto indexes
    for pattern in JUMP_PATTERNS:
        data = pattern.sub(goto_replacer, data)

    for i in range(len(original_messages)):
        assert original_messages[i] == translated_messages[i].original, \
                f'{blob}: Message mismatch: {original_messages[i]} and {translated_messages[i].original}'

    # Append translated messages
    message_indexes = [len(data)]
    for message in translated_messages:
        data += message.message.encode('cp936') + b'\x00'
        message_indexes.append(len(data))

    # Update message indexes
    i = 0
    data = bytearray(data)
    while i + MESSAGE_PREFIX_LEN + 4 < len(data):
        if MESSAGE_PREFIX_PATTERN.fullmatch(bytes(data[i:i+MESSAGE_PREFIX_LEN])):
            data[ i+MESSAGE_PREFIX_LEN : i+MESSAGE_PREFIX_LEN+4 ] = message_indexes.pop(0).to_bytes(4, 'little')
            i += MESSAGE_PREFIX_LEN + 4
        else:
            i += 1

    assert len(message_indexes) == 1, \
            f'{blob}: Not all message indexes were used. Remaining: {message_indexes}'

    with open(f'./data/translated_blob/{blob}', 'wb') as f:
        f.write(data)
