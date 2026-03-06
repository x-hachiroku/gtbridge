import re
import json
from sys import argv
from pathlib import Path
from gtbridge.tools.uif import UIF


uif = UIF()

def main():
    assert len(argv) == 4
    json_file, src_file, dst_file = argv[1:]

    with open(json_file) as f:
        replacements = json.load(f)

    with open(src_file, 'rb') as f:
        data = bytearray(f.read())

    for item in replacements:
        if 'address' not in item:
            continue

        addr = int(item['address'], 0)

        src = item['src'].encode('cp932')
        src_len = len(src)

        _dst = uif.replace(item['dst']).encode('cp932')
        dst = _dst.ljust(src_len, b'\x00')
        assert len(dst) == src_len, f'{hex(addr)} dst too long:\n{item["src"]}\n->\n{item["dst"]}'

        assert data[addr - 1] == 0, hex(addr)

        actual_src = data[addr:addr+src_len]
        assert actual_src == src, hex(addr)

        assert data[addr + src_len] == 0, hex(addr)

        data[addr:addr+src_len] = dst

    with open(dst_file, 'wb') as f:
        f.write(data)

if __name__ == '__main__':
    main()
