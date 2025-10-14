import json
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--extract', '-e', action='store_true', help='Extract messages from a message list')
    parser.add_argument('--inject', '-i', action='store_true', help='Inject messages back to message list')
    parser.add_argument('original')
    args = parser.parse_args()

    deduped_file = args.original[:-5] + '.dedup.json'

    if not (args.extract ^ args.inject):
        parser.print_help()
        exit(1)

    with open(args.original) as f:
        original = json.load(f)

    if args.extract:
        deduped = {}
        for message in original:
            deduped[(message['name'], message['original'])] = message
        with open(deduped_file, 'w') as f:
            json.dump(list(deduped.values()), f, indent=2, ensure_ascii=False)

    elif args.inject:
        with open(deduped_file) as f:
            deduped = json.load(f)
        deduped_dict = {(message['name'], message['original']): message for message in deduped}
        injected = [deduped_dict[(message['name'], message['original'])] for message in original]
        with open(args.original, 'w') as f:
            json.dump(injected, f, indent=2, ensure_ascii=False)
