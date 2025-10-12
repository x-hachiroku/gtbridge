import struct
import argparse

class Char:
    def __init__(self, byte_data, offset):
        self.offset = offset
        self.char = byte_data[1::-1].decode('cp932')
        self.coords = struct.unpack('<IIII', byte_data[4:20])
    def __str__(self):
        return f"{hex(self.offset)}\t{self.char}\t{self.coords}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    with open(args.filename, 'rb') as f:
        blob = f.read()

    chars = []
    ptr = blob.find(b'.tga') + 8

    while ptr < len(blob):
        char = Char(blob[ptr:ptr+28], ptr)
        chars.append(char)
        ptr += 28

    for char in chars:
        print(char)
