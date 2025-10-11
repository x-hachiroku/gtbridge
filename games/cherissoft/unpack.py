import struct
import argparse
from pathlib import Path

'''
4 bytes         | magic (\x41\x48\x46\x53)
4 bytes         | ?
4 bytes         | start of content section
\x3f terminated | \x7c separated | null-terminated | path
                  file entries   | 4 bytes         | size
                                 | 4 bytes         | offset
'''

class FileEntry:
    def __init__(self, path, size, offset):
        self.path = path
        self.size = size
        self.offset = offset
    def __str__(self):
        def human_readable_size(size):
            for unit in ['B', 'KiB', 'MiB', 'GiB']:
                if size < 1024:
                    return f"{size:.2f} {unit}"
                size /= 1024
            return f"{size:.2f} TiB"
        return f'{self.path}\t({human_readable_size(self.size)})'


class Archive:
    def __init__(self, archive_name):
        self.archive_name = archive_name
        self.files = []

        with open(self.archive_name, 'rb') as f:
            blob = f.read()

        eoh = struct.unpack('<I', blob[8:12])[0]
        assert blob[:4] == b'\x41\x48\x46\x53', 'Not a valid ARCHIVE file'
        assert blob[eoh-1] == 0x3f, 'Invalid header'

        self.entries_blob = blob[12:eoh-1]
        self.content_blob = blob[eoh:]

        ptr = 0
        while ptr < len(self.entries_blob):
            path_end = self.entries_blob.index(b'\x00', ptr)
            path = self.entries_blob[ptr:path_end].decode('cp932')
            size, offset = struct.unpack('<II', self.entries_blob[path_end + 1:path_end + 9])
            self.files.append(FileEntry(path, size, offset))
            ptr = path_end + 10

    def list(self):
        for entry in self.files:
            print(entry)

    def extract(self, entry):
        out_path = Path(entry.path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(self.content_blob[entry.offset:entry.offset + entry.size])
        print(f'Extracted {entry}')

    def extract_all(self):
        for entry in self.files:
            self.extract(entry)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', '-l', action='store_true', help='List files')
    parser.add_argument('filename', help='Archive filename')

    args = parser.parse_args()

    archive = Archive(args.filename)
    if args.list:
        archive.list()
    else:
        archive.extract_all()
