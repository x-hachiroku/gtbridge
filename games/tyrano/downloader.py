from loguru import logger
from pathlib import Path
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter

from gtbridge.games.tyrano.tyrano_parser import parse_line


BASE_URL = 'http://www.studio-beast.com/Suiside_Fence/web_ver/SF_web-epi1-/'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}

session = requests.Session()
session.headers.update(HEADERS)
session.mount('https://', HTTPAdapter(max_retries=3))


visited = set()

def get(path):
    if path.name[0] in {'&', '%'}:
        logger.warning(f'Unsolved storage reference: {path.name}')
        return

    if path in visited:
        return
    visited.add(path)

    if ',' in path.name:
        for p in path.name.split(','):
            get(path.parent / p.strip())
        return

    if path.exists():
        logger.debug(f'{path} exists, skipping...')
        if path.suffix == '.ks':
            parse(path.read_text())
        return

    url = urljoin(BASE_URL, str(path))
    try:
        logger.info(f'Getting {path}...')
        res = session.get(url)
        res.raise_for_status()
    except Exception as e:
        logger.error(f'Failed getting {url}: {e}')
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(res.content)

    if path.suffix == '.ks':
        parse(res.text)


def parse(content):
    for line in content.splitlines():
        line = line.strip()
        if not (cmd := parse_line(line)):
            continue

        if cmd['tag'] in {'button', 'glink'}:
            for key in cmd:
                if key ==  'storage':
                    get('data/scenario' / Path(cmd[key]))
                elif key == 'graphic' or 'img' in key:
                    if 'folder' in cmd:
                        get('data' / Path(cmd['folder']) / Path(cmd[key]))
                    else:
                        get('data/image' / Path(cmd[key]))
                elif 'se' in key:
                    get('data/sound' / Path(cmd[key]))

        elif cmd['tag'] == 'plugin':
            get(Path('data/others/plugin/' + cmd['name'] + '/init.ks'))

        elif cmd['tag'] == 'position' and 'frame' in cmd and len(cmd['frame']) > 0:
            get('data/image' / Path(cmd['frame']))

        elif 'storage' in cmd and len(cmd['storage']) > 0:
            storage = Path(cmd['storage'])

            if 'folder' in cmd:
                get('data' / Path(cmd['folder']) / storage)
                continue

            match cmd['tag']:
                case 'preload' | 'sysview':
                    get(storage)

                case 'image':
                    if 'layer' in cmd and cmd['layer'] in {'base', '0'}:
                        get('data/bgimage' / storage)
                    else:
                        get('data/fgimage' / storage)

                case 'graph' | 'cursor' | 'mask' | 'layermode':
                    get('data/image' / storage)

                case x if 'jump' in x or 'call' in x:
                    get('data/scenario' / storage)

                case x if 'movie' in x:
                    get('data/video' / storage)

                case x if 'bgm' in x:
                    get('data/bgm' / storage)
                case x if 'se' in x or 'voice' in x:
                    get('data/sound' / storage)

                case x if 'chara' in x:
                    get('data/fgimage' / storage)
                case x if 'bg' in x:
                    get('data/bgimage' / storage)

                case 'loadjs' | 'font' | 'deffont':
                    get('data/others' / storage)

                case _:
                    logger.warning(f'Unknown tag with storage: {line}. Assuming data dir.')
                    get('data' / storage)


if __name__ == '__main__':
    get(Path('data/system/Config.tjs'))
    get(Path('data/scenario/first.ks'))
