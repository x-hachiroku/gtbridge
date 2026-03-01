'''
Parser for encrypted `.loc` binary script files.

File structure (after stripping the 11-byte file header):
    - 11 bytes | Instruction
               | 4 bytes | sequence (?), uint32 LE
               | 3 bytes | op code
               | 4 bytes | argument length, uint32 LE

    - `argument length` bytes | CP932-encoded string

Encryption:
    Entire payload (instructions & arguments) after the file header is XOR-encrypted.
    The key is a single byte that rotates after every [argument + next-instruction] pair.

    Assuming the plain text of the most significant byte of argument length is always 0x00,
    i.e. `argument length` always less than 0x00ffffff, the keys can be retrived by:

        1. key_1 = MSB of argument_1 length from instruction_1
        2. Decrypt instruction_1 with key_1, get length of argument_1, thus offset of instruction_2
        3. key_2 = MSB of argument_2 length from instruction_2
        and so on...
'''

import struct
from pathlib import Path


def _xor(data: bytes, key: int) -> bytes:
    '''XOR every byte in *data* with the single-byte *key*.'''
    return bytes(b ^ key for b in data)


class LOC:
    HEADER_LEN      = 11 # file-level header, skipped entirely
    INSTRUCTION_LEN = 11

    COUNTER_OFFSET = 0
    CODE_OFFSET    = 4
    ARGLEN_OFFSET  = 7

    TEXT_CODES = (b'\x00\x01\x02',)

    class Segment:
        def __init__(self,
             sequence: int,
             key: int,
             code: bytes,
             argument: bytes = b'',
         ):
            self.sequence = sequence
            self.key      = key
            self.code     = code
            self.argument = argument

        def get_text(self) -> str:
            if self.code in LOC.TEXT_CODES:
                return self.argument.decode('cp932')
            return ''

        def set_text(self, text: str):
            if self.code in LOC.TEXT_CODES:
                self.argument = text.encode('cp932')
            else:
                raise ValueError(f'Instruction code {self.code.hex()} does not support text argument.')

        def __repr__(self) -> str:
            _repr = f'LOC.Segment(sequence={self.sequence}, key={hex(self.key)}, code={self.code.hex()}, '
            if self.code in LOC.TEXT_CODES:
                _repr += f'text={repr(self.get_text())}'
            else:
                _repr += f'argument={self.argument.hex()}'
            _repr += ')'
            return _repr


    def __init__(self, header: bytes, segments: list[Segment]):
        self.header    = header   # the 11-byte file header, stored verbatim
        self.segments  = segments # ordered list of LOC.Segment objects

    @staticmethod
    def _decode_instr(raw_instr: bytes, key: int) -> tuple[int, bytes, int]:
        dec     = _xor(raw_instr, key)
        sequence = struct.unpack_from('<I', dec, LOC.COUNTER_OFFSET)[0]
        code    = dec[LOC.CODE_OFFSET:LOC.CODE_OFFSET + 3]
        arg_len = struct.unpack_from('<I', dec, LOC.ARGLEN_OFFSET)[0]
        return sequence, code, arg_len

    @staticmethod
    def _encode_instr(sequence: int, code: bytes, arg_len: int, key: int) -> bytes:
        buf = bytearray(LOC.INSTRUCTION_LEN)
        struct.pack_into('<I', buf, LOC.COUNTER_OFFSET, sequence)
        buf[LOC.CODE_OFFSET:LOC.CODE_OFFSET + 3] = code
        struct.pack_into('<I', buf, LOC.ARGLEN_OFFSET, arg_len)
        return _xor(bytes(buf), key)

    @classmethod
    def from_bytes(cls, data: bytes):
        header = data[:LOC.HEADER_LEN]
        raw    = data[LOC.HEADER_LEN:]
        pos    = 0
        total  = len(raw)
        segments = []

        key = raw[10]

        while True:
            ## Decrypt the current instruction block.
            instruction_raw = raw[pos : pos+LOC.INSTRUCTION_LEN]
            assert len(instruction_raw) == LOC.INSTRUCTION_LEN

            sequence, code, arg_len = LOC._decode_instr(instruction_raw, key)
            pos += LOC.INSTRUCTION_LEN


            next_instruction_pos = pos + arg_len
            if next_instruction_pos == total:
                segments.append(LOC.Segment(sequence=sequence, key=key, code=code))
                break

            next_key = raw[next_instruction_pos + LOC.INSTRUCTION_LEN - 1]
            arg_raw = raw[pos: pos + arg_len]
            argument = _xor(arg_raw, next_key)
            segments.append(LOC.Segment(sequence=sequence, key=key, code=code, argument=argument))

            pos = next_instruction_pos
            key = next_key

        return cls(header=header, segments=segments)


    @classmethod
    def from_file(cls, path: str | Path):
        return cls.from_bytes(Path(path).read_bytes())


    def encode(self) -> bytes:
        raw_payload = bytearray()

        key = self.segments[0].key

        for i, seg in enumerate(self.segments):
            arg_bytes   = seg.argument
            arg_len     = len(arg_bytes)

            raw_payload += LOC._encode_instr(seg.sequence, seg.code, arg_len, key)

            if i+1 < len(self.segments):
                next_key = self.segments[i+1].key

                raw_payload += _xor(arg_bytes, next_key)
                key = next_key

        return self.header + bytes(raw_payload)


if __name__ == '__main__':
    import sys

    path = sys.argv[1]
    loc = LOC.from_file(path)
    for seg in loc.segments:
        print(seg)
    print(f'Total segments: {len(loc.segments)}\n')

    original = Path(path).read_bytes()
    reencoded = loc.encode()
    assert original == reencoded
