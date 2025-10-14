import struct
from pathlib import Path

'''
2 bytes        | file count
1 byte         | filename length
4 bytes        | start of contents section
until contents | file entries | [filename length] | path
                              | 4 bytes           | offset
                              | 4 bytes           | size
'''

class FileEntry:
    def __init__(self, path='', size=0, offset=0):
        self.path = path
        self.offset = offset
        self.size = size

    @classmethod
    def from_bytes(cls, data, filename_len):
        path = data[:filename_len].decode('cp932').rstrip('\x00')
        offset, size = struct.unpack('<II', data[filename_len:])
        return cls(path, size, offset)

    def to_bytes(self, filename_len):
        name_bytes = self.path.encode('cp932')
        assert len(name_bytes) <= filename_len, self.path
        name_bytes = name_bytes.ljust(filename_len, b'\x00')
        return name_bytes + struct.pack('<II', self.offset, self.size)

    def __str__(self):
        def human_readable_size(size):
            for unit in ['B', 'KiB', 'MiB']:
                if size < 1024:
                    return f"{size:.2f} {unit}"
                size /= 1024
            return f"{size:.2f} GiB"
        return f'{self.path}\t({human_readable_size(self.size)})'


class PAC:
    def __init__(self, name):
        self.name = name
        self.filename_len = 0
        self.file_entries = []
        self.contents_blob = bytearray()

    @classmethod
    def from_file(cls, path):
        path = Path(path)
        blob = path.read_bytes()
        file_count, filename_len, eoh = struct.unpack('<HBI', blob[0:7])

        inst = cls(name=path.name)
        inst.filename_len = filename_len
        entries_blob = blob[7:eoh]
        inst.contents_blob = blob[eoh:]

        entry_size = filename_len + 8
        for i in range(0, len(entries_blob), entry_size):
            entry_data = entries_blob[i:i + entry_size]
            inst.file_entries.append(FileEntry().from_bytes(entry_data, filename_len))
        assert len(inst.file_entries) == file_count

        return inst

    @staticmethod
    def swap_nibbles(byte):
        return ((byte << 4) & 0xFF) | (byte >> 4)

    @staticmethod
    def decode_srp(data):
        data = bytearray(data)
        for ptr in range(len(data)):
            data[ptr] = PAC.swap_nibbles(data[ptr] ^ 0x0A)
        return data

    @staticmethod
    def encode_srp(data):
        data = bytearray(data)
        for ptr in range(len(data)):
            data[ptr] = PAC.swap_nibbles(data[ptr]) ^ 0x0A
        return data

    def list(self):
        for entry in self.file_entries:
            print(entry)

    def extract(self, entry, decode):
        out_path = Path(entry.path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        data = self.contents_blob[entry.offset:entry.offset + entry.size]
        if decode:
            data = PAC.decode_srp(data)
        out_path.write_bytes(data)
        print(f'Extracted {entry}')

    def extract_all(self, decode=False):
        if self.name == 'srp.pac':
            decode = True
        for entry in self.file_entries:
            self.extract(entry, decode)

    def add(self, filename, data):
        self.filename_len = max(self.filename_len, len(filename))
        self.file_entries.append(FileEntry(filename, len(data), len(self.contents_blob)))
        if self.name == 'srp.pac':
            data = PAC.encode_srp(data)
        self.contents_blob += data

    def add_dir(self, path):
        path = Path(path)

        for full_path in path.rglob('*'):
            relative_path = full_path.relative_to(path).as_posix()
            data = full_path.read_bytes()
            self.add(relative_path, data)

    def to_file(self, out_path):
        file_count = len(self.file_entries)
        eoh = 7 + file_count * (self.filename_len + 8)
        header = struct.pack('<HBI', file_count, self.filename_len, eoh)

        entries_blob = b''.join(entry.to_bytes(self.filename_len) for entry in self.file_entries)

        with open(out_path, 'wb') as f:
            f.write(header + entries_blob + self.contents_blob)

        return out_path


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--list', '-l', action='store_true', help='list archive contents')
    parser.add_argument('--pack', '-p', metavar='dir', help='pack pac from dir')
    parser.add_argument('filename', nargs='?', help='archive filename')
    args = parser.parse_args()

    if args.pack:
        if not args.filename:
            out_path = Path(args.pack).with_suffix('.pac')
        else:
            out_path = Path(args.filename)

        pac = PAC(name=out_path.name)
        pac.add_dir(args.pack)
        pac.to_file(out_path)

    else:
        if not args.filename:
            parser.print_help()
            exit(1)
        pac = PAC.from_file(args.filename)

        if args.list:
            pac.list()
        else:
            pac.extract_all()
