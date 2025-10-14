import json
from pathlib import Path
import argparse


def dedupe(srcs):
    message_map = {}
    original_map = {}
    for src in srcs:
        with open(src) as f:
            original = json.load(f)
        for message in original:
            key = (message['name'], message['message'])
            original_map[(message['name'], message['original'])] = (message['name'], message['message'])
            message_map[key] = message

    return message_map.values(), original_map


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
        srcs = list(Path(args.src).rglob('*.json'))
    else:
        srcs = [Path(args.src)]

    if args.extract:
        deduped, _ = dedupe(srcs)
        with open(args.src+'.deduped.json', 'w') as f:
            json.dump(list(deduped), f, indent=2, ensure_ascii=False)

    elif args.inject:
        _, original_map = dedupe(srcs)
        deduped_dict = {}

        with open(args.src+'.deduped.json') as f:
            deduped = json.load(f)

        for message in deduped:
            key = original_map.get((message['name'], message['original']))
            if key:
                deduped_dict[key] = message

        for src in srcs:
            with open(src) as f:
                original = json.load(f)
            for i, message in enumerate(original):
                if translated := deduped_dict.get((message['name'], message['message'])):
                    original[i]['message'] = translated['message']
                elif message['message']:
                    print(f"Warning: Message not found: {src}: {message['name']}: {message['original']}")
            with open(src, 'w') as f:
                json.dump(original, f, indent=2, ensure_ascii=False)
