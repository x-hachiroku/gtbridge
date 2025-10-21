import argparse
from gtbridge.tools.uif import UIF

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--recover', action='store_true')
    parser.add_argument('text')

    args = parser.parse_args()
    uif = UIF()

    if args.recover:
        print(uif.recover(args.text))
    else:
        print(uif.replace(args.text))
