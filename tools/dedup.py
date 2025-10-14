import json
from pathlib import Path
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--extract', '-e', action='store_true', help='Extract messages from a message list')
    parser.add_argument('--inject', '-i', action='store_true', help='Inject messages back to message list')
    parser.add_argument('--recursive', '-r', action='store_true', help='Process directories recursively')
    parser.add_argument('src')
    args = parser.parse_args()

    if not (args.extract or args.inject):
        parser.print_help()
        exit(1)

    if args.recursive:
        srcs = Path(args.src).rglob('*.json')
    else:
        srcs = [Path(args.src)]

    if args.extract:
        deduped = {}
        for src in srcs:
            with open(src) as f:
                original = json.load(f)
            for message in original:
                deduped[(message['name'], message['original'])] = message
        with open(args.src+'.deduped.json', 'w') as f:
            json.dump(list(deduped.values()), f, indent=2, ensure_ascii=False)

    elif args.inject:
        with open(args.src+'.deduped.json') as f:
            deduped = json.load(f)
        deduped_dict = {(message['name'], message['original']): message for message in deduped}
        for src in srcs:
            with open(src) as f:
                original = json.load(f)
            injected = [deduped_dict[(message['name'], message['original'])] for message in original]
            with open(src, 'w') as f:
                json.dump(injected, f, indent=2, ensure_ascii=False)
