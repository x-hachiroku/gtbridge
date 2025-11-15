import struct
from pathlib import Path

original_path = Path('./data/original')
translated_path = Path('./data/translated')

DATA_START_ADDR = 0x4B026E
DATA_TAIL = b'\x7f\x7f\x00\x00\x00\x00\x00\x00'


def main(pack, process_all):
    with open(original_path/'mextasy.exe', 'rb') as f:
        data = f.read()

    data = bytearray(data)
    ptr = DATA_START_ADDR

    while ptr < len(data) - len(DATA_TAIL):
        path_len = struct.unpack_from('<H', data, ptr)[0]
        ptr += 2

        path = data[ptr:ptr+path_len].decode('cp932')
        ptr += path_len

        assert path[:3] == 'C:\\'
        local_path = path[3:].replace('\\', '/')

        file_size = struct.unpack_from('<I', data, ptr)[0]
        ptr += 4

        if not process_all and not local_path.startswith('AVG_HWA/scenario/'):
            print(f'Skipped: {local_path}')
            ptr += file_size
            continue

        if pack:
            file_data = (translated_path / local_path).read_bytes()
            file_data = file_data.ljust(file_size, b'\x00')
            assert len(file_data) == file_size, local_path
            data[ptr:ptr+file_size] = file_data
            print(f'Packed: {local_path} (offset {ptr})')

        else:
            file_data = data[ptr:ptr+file_size]
            out_path = original_path / local_path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(file_data)
            print(f'Extracted: {out_path} (offset {ptr})')

        ptr += file_size

    assert data[ptr:] == DATA_TAIL


    if pack:
        (translated_path / 'mextasy.exe').write_bytes(data)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['p', 'e'])
    parser.add_argument('--all', '-a', action='store_true',
                        help='Process all files, by default only scenriao dir is processed')
    args = parser.parse_args()

    main(args.mode == 'p', args.all)
