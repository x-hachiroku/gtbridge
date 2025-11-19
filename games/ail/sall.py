import re
import struct

'''
4 bytes         | \0\0\0\0
2 bytes         | pages index lne
2 bytes         | pages len
2 bytes         | texts len
2 bytes         | \0\0
pages index len | page indexes  | 2 bytes index
                                | 2 bytes offset
pages len       | pages
texts len       | texts
'''

class TextBase:
    class Entry:
        def __init__(self, text_bytes, sequence):
            self.text_bytes = text_bytes
            self.accessed = False
            self.sequence = sequence

    def __init__(self, texts_bytes, encoding='cp932'):
        self.texts_bytes = texts_bytes
        self.encoding = encoding
        self.last_sequence = 0

        self.entries = {}
        offset = 0
        for i, t in enumerate(texts_bytes.split(b'\x00\x00')[:-1]):
            self.entries[struct.pack('>H', offset)] = TextBase.Entry(t, i)
            offset += len(t) + 2

    def get(self, offset):
        entry = self.entries.get(offset)
        if entry:
            if entry.sequence > (self.last_sequence + 1):
                print(f'Warning: Out of order access: {entry.text_bytes.decode(self.encoding).strip()}')
            entry.accessed = True
            self.last_sequence = max(self.last_sequence, entry.sequence)
            return entry.text_bytes.decode(self.encoding).strip()

        start = struct.unpack('>H', offset)[0]
        if start > len(self.texts_bytes):
            print(f'Warning: Invalid text offset {offset.hex()}')
            return
        end = self.texts_bytes.find(b'\x00\x00', start)
        if end == -1:
            end = len(self.texts_bytes)
        text = self.texts_bytes[start:end].decode(self.encoding).strip()
        print(f'Warning: Partial text referenced:: {text}')
        return text

    def get_orphaned(self):
        texts = []
        for entry in self.entries.values():
            if not entry.accessed and entry.text_bytes.strip(b'\x00'):
                texts.append(entry.text_bytes.decode(self.encoding).strip())
        return texts


class Page:
    PATTERNS = {
        re.compile(k, re.DOTALL): v for k, v in {
            rb'\x00[\x00\x01]\xFF[\x00-\x1F]([^\xFF].)': '',
            rb'\x00\x00\x05\xFF\xFF([^\xFF].)\x0E': 'OPTION',
            rb'\x00\x00\x01\x00\x0F([^\xFF].)': 'OPTION',
            rb'\x00\x6E([^\xFF].)\xFF[\x00\x01]': 'TITLE',
            rb'[\x00\xFF][\x01-\x1F]\xFF\x00\xFF\x00\xFF\x00([^\xFF].)': 'TITLE',
            rb'\xFF\x00\xFF\x00\xFF\x0A([^\xFF].)': 'TITLE',
        }.items()
    }

    def __init__(self, page_bytes, textbase):
        self.page_bytes = page_bytes
        self.texts = {}

        ptr = 0
        while ptr <= len(page_bytes):
            for pattern, label in Page.PATTERNS.items():
                if match := pattern.match(page_bytes[ptr:]):
                    index = match.group(1)
                    if text := textbase.get(index):
                        if label:
                            self.texts[-1] = f'【{label}】'
                        self.texts[ptr + match.start(1)] = text
                        ptr += match.end() - 1
                    break
            ptr += 1

    def get_texts(self):
        return list(self.texts.values())

    def set_texts(self, texts):
        texts += [''] * (len(self.texts) - len(texts))
        assert len(self.texts) == len(texts), (self.texts, texts)
        for ptr, text in zip(self.texts.keys(), texts):
            self.texts[ptr] = text


class SALL:
    def __init__(self, data):
        self.len = len(data)

        page_offsets_len, pages_len, texts_len = struct.unpack_from('<HHH', data, 4)
        page_offsets_bytes = data[ 12 : 12+page_offsets_len ]
        pages_bytes = data[ 12+page_offsets_len : 12+page_offsets_len+pages_len ]
        text_bytes = data[ 12+page_offsets_len+pages_len : ]
        assert len(text_bytes) == texts_len

        page_offsets = [
            struct.unpack_from('<H', page_offsets_bytes, i)[0]
            for i in range(2, page_offsets_len, 4)
        ]

        self.header_bytes = data[ : 12+page_offsets_len ]
        self.textbase = TextBase(text_bytes)

        self.pages = []
        for i in range(len(page_offsets)):
            end = page_offsets[i+1] if i+1 < len(page_offsets) else len(pages_bytes)
            page_bytes = pages_bytes[page_offsets[i]:end]
            self.pages.append(Page(page_bytes, self.textbase))

    def to_bytes(self, encoding='cp932'):
        data = bytearray(self.header_bytes)
        text_bytes = bytearray()

        for page in self.pages:
            page_bytes = bytearray(page.page_bytes)
            for ptr, text in page.texts.items():
                if ptr != -1:
                    page_bytes[ptr:ptr+2] = struct.pack('>H', len(text_bytes))
                    text_bytes += text.encode(encoding) + b'\x00\x00'
            data += page_bytes

        data += text_bytes
        struct.pack_into('<H', data, 8, len(text_bytes))

        return data
