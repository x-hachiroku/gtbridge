import os
import json
import argparse
from pathlib import Path

def dump_names(names, filename):
    name_dict = {}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            name_dict = json.load(f)

    for name in sorted(names, key=names.get, reverse=True):
        if name not in name_dict:
            name_dict[name] = name

    with open(filename, 'w') as f:
        json.dump(name_dict, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inject', '-i', action='store_true')
    parser.add_argument('--extract', '-e', action='store_true')
    args = parser.parse_args()

    if args.extract:
        names = {}
        for src in Path('.').rglob('*.json'):
            if src.name == 'names.json':
                continue
            with open(src, 'r') as infile:
                file_data = json.load(infile)
            for message in file_data:
                if 'name' in message:
                    if message['name'] not in names:
                        names[message['name']] = 0
                    names[message['name']] += 1
        dump_names(names, 'names.json')

    elif args.inject:
        if not os.path.exists('names.json'):
            print('`names.json` not found.')
            exit(1)

        with open('names.json', 'r') as f:
            name_dict = json.load(f)

        not_found = set()
        for src in Path('.').rglob('*.json'):
            if src.name == 'names.json':
                continue
            with open(src, 'r') as infile:
                file_data = json.load(infile)
            for message in file_data:
                if 'name' in message:
                    if message['name'] in name_dict:
                        message['name'] = name_dict[message['name']]
                    else:
                        not_found.add(message['name'])
            with open(src, 'w') as outfile:
                json.dump(file_data, outfile, ensure_ascii=False, indent=2)
        if not_found:
            for name in not_found:
                print(f'{name} not found in names.json')
