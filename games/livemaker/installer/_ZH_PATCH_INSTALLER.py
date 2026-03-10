from os import listdir
from livemaker.cli.lmpatch import lmpatch

if __name__ == '__main__':
    target = ''
    for f in listdir('.'):
        if f.endswith('.exe') or f.endswith('.ext'):
            target = f

    if target:
        print('Patcing', target)
        lmpatch.main(args=[target, '-r', '_ZH_PATCH_ASSETS'])
        print('Patch installed')
    else:
        print('Fatal: No exe/ext found')

    input('Press enter to exit')
