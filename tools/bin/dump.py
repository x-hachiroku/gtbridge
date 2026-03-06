import re
import json
from sys import argv
from gtbridge.message import VALID_JA_PATTERN

CONTROL_CHAR_PATTERN = re.compile(r'[\x00-\x08\x11-\x1F\x7F]')
TEXT_PATTERN = re.compile(b'(?<=\x00)([^\x00]{4,})(?=\x00)', re.DOTALL)

def get_string(raw_bytes):
    try:
        text = raw_bytes.decode('cp932')

        if CONTROL_CHAR_PATTERN.search(text):
            return ''

        if VALID_JA_PATTERN.search(text):
            return text

    except UnicodeDecodeError:
        return ''


if __name__ == '__main__':
    with open(argv[1], 'rb') as f:
        data = f.read()

    strings = []

    for match in TEXT_PATTERN.finditer(data):
        raw_bytes = match.group(1)
        address = match.start(1)
        text = get_string(raw_bytes)

        if address < 0x82adf:
            continue

        if text:
            strings.append({
                'address': hex(address),
                'original': text,
                'message': text,
            })

    print(json.dumps(strings, ensure_ascii=False, indent=2))
