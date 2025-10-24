import json
from pathlib import Path

from gtbridge import MessageList
from gtbridge.games.mai.sct import SCT

SCT_DICT = {
    'main.sct': (0xD031, 0xF02F),
    'scene.sct': (0xCB51, 0xDB96),
}

FN, SN = '和倉', '創太'

NAMES = {
  '_vFnsn': SN,
  '_vEtcs': '？？？',
  '_vKara': 'しおから',
  '_vKiyu': '希由子',
  '_vMaki': '牧恵',
  '_vMiri': 'ミリオム',
  '_vTosi': '鋭章',
  '_vYuzu': '柚紀'
}


if __name__ == '__main__':
    blob_path = Path('./data/original_blob/')
    json_path = Path('./data/original_json/')

    message_list = MessageList()
    for s in SCT_DICT:
        json_subpath = json_path / s[:-4]
        json_subpath.mkdir(parents=True, exist_ok=True)

        sct = SCT((blob_path/s).read_bytes(), *SCT_DICT[s])

        for chunk in sct.chunks:
            name = ''
            for message in chunk.get_messages():
                if message and message[0] == '_':
                    name = NAMES.get(message, '')
                    continue

                original = message
                message = message.replace('#fn', FN).replace('#sn', SN)

                if len(message) >= 2 and message[-2] == '#':
                    post = message[-2:]
                    message = message[:-2]
                else:
                    post = ''

                if '#' in message:
                    print(f'Warning: unresolved control code in message: {message}')

                message_list.append(message, original=original, name=name, post=post)
                name = ''

            message_list.flush((json_subpath / chunk.name).with_suffix('.json'))

    message_list.dump_stats('')
