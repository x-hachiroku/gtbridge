class SRPEntry:
    TYPE_TITLE = b'\xA1'
    TYPE_TEXT = b'\x14'
    TYPE_VOICE = b'\x17'
    TYPE_SELECTION = b'\x23'
    TYPE_ACTION = b'\x31'
    TYPE_HCG = b'\xCA'

    SELECTION_PREFIX = b'\x14'
    ACTION_LENGTH = 10
    ACTION_PREFIX = b'\x30\x30\x31'
    ACTION_HEADER_LENGTH = 8
    OPTION_PREFIX = b'\x20\x14\x01'
    HCG_HEADER_LENGTH_DICT = { b'\x15': 4, b'\x1A': 5 }

    def __init__(self, payload, encoding='cp932'):
        self.type = payload[0:1]
        self.data = payload[1:]

        self._options = None
        self._action = None
        self._hcg = None
        self.name = ''
        self.text = ''
        self._length = 0
        self._voice = ''

        match self.type:
            case SRPEntry.TYPE_TITLE:
                self.name = 'TITLE'
                self.text = self.data.decode(encoding)

            case SRPEntry.TYPE_TEXT:
                self.text = self.data.decode(encoding)

            case SRPEntry.TYPE_VOICE:
                 self._voice, self.name, self.text = self.data.decode(encoding).split(',')

            case SRPEntry.TYPE_SELECTION:
                assert self.data[0:1] == SRPEntry.SELECTION_PREFIX

                self._options = {}
                for option in self.data[2:].split(SRPEntry.OPTION_PREFIX)[1:]:
                    assert option
                    option_text, option_label = option.decode(encoding).split(',')
                    self._options[option_label] = option_text
                count = self.data[1]
                assert count == len(self._options)

                self.name = 'OPTIONS'
                self.text = '\n'.join(self._options.values())

            case SRPEntry.TYPE_ACTION:
                if self.data[0:3] == SRPEntry.ACTION_PREFIX:
                    self._action = self.data[SRPEntry.ACTION_HEADER_LENGTH:].decode(encoding).split(',')
                    assert len(self._action) == 3 and len(self._action[1].encode(encoding)) == SRPEntry.ACTION_LENGTH
                    self.name = 'ACTION'
                    self.text = self._action[1].rstrip('　')

            case SRPEntry.TYPE_HCG:
                if self.data[0:1] in SRPEntry.HCG_HEADER_LENGTH_DICT:
                    prefix_length = SRPEntry.HCG_HEADER_LENGTH_DICT[self.data[0:1]]
                    self._hcg = self.data[prefix_length:].decode(encoding).split(' ')
                    self._length = len(self._hcg[0].encode(encoding))
                    self.name = 'SCENE'
                    self.text = self._hcg[0].rstrip('　')

    def to_bytes(self, encoding='cp936'):
        def byte_ljust(s, length, encoding, fillchar='　'):
            l = len(s.encode(encoding))
            assert l%2 == 0 and l <= length, s
            return s + fillchar * ((length - l) // len(fillchar.encode(encoding)))

        match self.type:
            case SRPEntry.TYPE_TEXT | SRPEntry.TYPE_TITLE:
                self.data = self.text.encode(encoding)

            case SRPEntry.TYPE_VOICE:
                self.data = f'{self._voice},{self.name},{self.text}'.encode(encoding)

            case SRPEntry.TYPE_SELECTION:
                options = self.text.split('\n')
                assert len(options) == len(self._options)
                for i, key in enumerate(self._options.keys()):
                        self._options[key] = options[i]
                encoded = bytearray()
                encoded += SRPEntry.SELECTION_PREFIX
                encoded += len(self._options).to_bytes(1)
                for label, text in self._options.items():
                    encoded += SRPEntry.OPTION_PREFIX
                    encoded += f'{text},{label}'.encode(encoding)
                self.data = bytes(encoded)

            case SRPEntry.TYPE_ACTION:
                if self._action:
                    self._action[1] = byte_ljust(self.text, SRPEntry.ACTION_LENGTH, encoding)
                    _action = ','.join(self._action)
                    self.data = self.data[:SRPEntry.ACTION_HEADER_LENGTH] + _action.encode(encoding)

            case SRPEntry.TYPE_HCG:
                if self._hcg:
                    prefix_length = SRPEntry.HCG_HEADER_LENGTH_DICT[self.data[0:1]]
                    self._hcg[0] = byte_ljust(self.text, self._length, encoding)
                    _hcg = ' '.join(self._hcg)
                    self.data = self.data[:prefix_length] + _hcg.encode(encoding)

        return self.type + self.data


class SRP:
    def __init__(self, path, encoding='cp932'):
        with open(path, 'rb') as f:
            data = f.read()

        chunks = data.split(b'\x00')
        assert chunks, path

        self.header = chunks.pop(0)

        self.entries = []
        for chunk in chunks:
            self.entries.append(SRPEntry(chunk, encoding))

    def write(self, path, encoding='cp936'):
        entries_bytes = b'\x00'.join(e.to_bytes(encoding) for e in self.entries)
        data = self.header + b'\x00' + entries_bytes

        with open(path, 'wb') as f:
            f.write(data)


if __name__ == '__main__':
    from pathlib import Path

    src = Path('data/original_srp')
    dst = Path('data/srp_test')
    for srp in src.glob('*'):
        output_path = dst / srp.relative_to(src)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        SRP(srp).write(output_path, 'cp932')
