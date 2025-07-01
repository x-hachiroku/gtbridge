import re

NOTICE = '指定されたラベルは見つかりませんでした。'
CTRL_TEXT_PATTERN = re.compile(r'[0-9A-Za-z._:\\]*', re.DOTALL)

MESSAGE_PATTERN = re.compile(
    b'\x7F\x00\x00\x00'
    b'...\x00' # Text header index
    b'..\x00\x00' # Inst seq (?)
    b'\x03\x00\x00\x00'
    b'(....)' # Text index
    b'(?:\x03\x00\x00\x00(....))?' + # Name index
    b'\x00' * 12,
    re.DOTALL
)

TITLE_PATTERN = re.compile(
    b'\x7F\x00\x00\x00'
    b'...\x00'
    b'..\x00\x00'
    b'\x03\x00\x00\x00'
    b'(....)'
    + re.escape(b'\x3F\x00\x00\x00') + # \x3F=`?`
    b'\x01\x00\x00\x00',
    re.DOTALL
)

ALIAS_PATTERN = re.compile(
    b'\x7F\x00\x00\x00'
    b'...\x00'
    b'..\x00\x00'
    b'\x03\x00\x00\x00'
    b'....' # Name
    b'\x03\x00\x00\x00'
    b'(....)' # Alias
    + re.escape(b'\x3F\x00\x00\x00'
    b'\x02\x00\x00\x00'
    b'\x5E\x01\x00\x00'), # \x5E=`^`
    re.DOTALL
)

OPTION_PATTERN = re.compile(b'\x20\x00\x00\x00\x03\x00\x00\x00(....)', re.DOTALL)

FURIGANA_PATTERN = re.compile( r'<ruby ([^,]+),([^>]+)>', re.DOTALL)
VALID_FURIGANAS = {
    '・',
    'ここ',
    'プリズム',
    'エルドラド',
    'プリズム・リズム',
}


class Script():
    def __init__(self, blob):
        self.blob = blob
        self.title_index = 0
        self.texts = {}
        self.used_indexes = set()

        with open(f'./data/original_blob/{blob}', 'rb') as f:
            _data = f.read()

        if match := TITLE_PATTERN.search(_data):
            self.title_index = int.from_bytes(match.group(1), 'little')

            self.header_bytes       = _data[:0x50]
            self.instructions_bytes = _data[0x50:self.title_index+0x50]
            self.texts_bytes        = _data[self.title_index+0x50:]

            current_index = self.title_index
            for text_bytes in self.texts_bytes.split(b'\x00'):
                text = text_bytes.decode('cp932')
                self.texts[current_index] = text
                current_index += len(text_bytes) + 1

    @property
    def title(self):
        self.used_indexes.add(self.title_index)
        return self.texts[self.title_index]

    def get_text(self, index_bytes):
        index = int.from_bytes(index_bytes, 'little')
        self.used_indexes.add(index)
        return self.texts[index]

    def check_used(self):
        for index, text in self.texts.items():
            if index not in self.used_indexes:
                if text != NOTICE and not CTRL_TEXT_PATTERN.fullmatch(text):
                    print(f'{self.blob} unused text: {hex(index)} {text}')


if __name__ == '__main__':
    print('Message pattern:', MESSAGE_PATTERN.pattern)
    print('Title pattern:', TITLE_PATTERN.pattern)
    print('Alias pattern:', ALIAS_PATTERN.pattern)
