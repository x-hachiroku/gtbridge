import argparse
from gtbridge import load

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-b', action='store_true', help='Use bytes')
args = parser.parse_args()

data = load(args.file)
for message in data:
    if args.b:
        lm = len(message.message.encode('cp936'))
        lo = len(message.original.encode('cp932'))
    else:
        lm = len(message.message)
        lo = len(message.original)
    if lm > lo:
        print(f'Message longer than original:\n{message.original}\n{message.message}\n')
