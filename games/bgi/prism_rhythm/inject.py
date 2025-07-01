import os
import json
from message import load
from patterns import *


if not os.path.isdir('./data/translated_blob'):
    os.mkdir('./data/translated_blob')

with open('./names.json', 'r') as f:
    names_table = json.load(f)

for blob in os.listdir('./data/original_blob'):
    if blob == 'select':
        continue
    if not os.path.exists(f'./data/translated_json/{blob}.json'):
        print(f'{blob}: no translation found, skipping')
        continue

    s = Script(blob)

    _index_table = {}
    texts_table = { m.original : m.message for m in load(f'./data/translated_json/{blob}.json') }
    texts_table.update(names_table)
    translated_texts_bytes = b''
    for i, text in s.texts.items():
        _index_table[i] = s.title_index +  len(translated_texts_bytes)
        if text in texts_table:
            translated_texts_bytes += texts_table[text].encode('cp936') + b'\x00'
        else:
            translated_texts_bytes += text.encode('cp936') + b'\x00'
    index_table = { k.to_bytes(4, 'little') : v.to_bytes(4, 'little') for k, v in _index_table.items() }

    i = 0
    instructions_bytearray = bytearray(s.instructions_bytes)
    while i + 8 <= len(instructions_bytearray):
        if instructions_bytearray[i:i+4] == b'\x03\x00\x00\x00':
            index = bytes(instructions_bytearray[i+4:i+8])
            if int.from_bytes(index, 'little') > s.title_index:
                instructions_bytearray[i+4:i+8] = index_table[index]
                i += 4
        i += 4

    with open(f'./data/translated_blob/{blob}', 'wb') as f:
        f.write(s.header_bytes + instructions_bytearray + translated_texts_bytes)


with open('./data/original_blob/select', 'rb') as f:
    _data = f.read()

original_header_bytes = _data[:0x5ecb]
original_options_bytes = _data[0x5ecb:]

translated_options = load('./data/translated_json/select.json')

translated_header_bytearray = bytearray(original_header_bytes)
translated_options_bytes = b''
base_index = 0x5d0b

for match in OPTION_PATTERN.finditer(original_header_bytes):
    translated_option = translated_options.pop(0)
    original_option_start = int.from_bytes(match.group(1), 'little') - base_index
    original_option_end = original_options_bytes.find(b'\x00', original_option_start)
    original_option = original_options_bytes[original_option_start:original_option_end].decode('cp932')
    assert original_option == translated_option.original, f'Option mismatch: {original_option}|{translated_option.original}'

    len_diff = len(original_option) - len(translated_option.message)
    assert len_diff >= 0, f'Option translation too long: {translated_option.original}|{translated_option.message}'
    if len_diff %2 != 0:
        translated_option.message = ' ' + translated_option.message + ' '
        len_diff -= 1
    translated_option.message = '　' * (len_diff//2)  + translated_option.message + '　' * (len_diff//2)
    # translated_header_bytearray[match.start(1):match.end(1)] = (base_index + len(translated_options_bytes)).to_bytes(4, 'little')
    translated_options_bytes += translated_option.message.encode('cp936') + b'\x00'

with open('./data/translated_blob/select', 'wb') as f:
    f.write(translated_header_bytearray + translated_options_bytes)
