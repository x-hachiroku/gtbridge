import json
from pathlib import Path

from gtbridge import MessageList
from gtbridge.games.mai.sct import SCT

SCT_DICT = {
    'main.sct': (0x1EE31, 0x226CB),
    'scene.sct': (0x1EE31, 0x1FF25),
}

NAMES = {
    '_vAzus': '梓',
    '_vEtcs': '？？？',
    '_vFnsn': 'ぷーさん',
    '_vHide': '英美',
    '_vMako': '麻亜子',
    '_vMisa': '美沙',
    '_vMixs': '一同',
    '_vNeko': '猫柳氏',
    '_vRusi': 'ルーシー',
    '_vSara': 'サラ',
    '_vTama': 'たまえ',
    '_vTomo': 'ともよ',
    '_vYuka': 'ゆかり',
    '_vYuri': 'ゆりあ'
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

                if len(message) >= 2 and message[-2] == '#':
                    post = message[-2:]
                    message = message[:-2]
                else:
                    post = ''

                message_list.append(message, name=name, post=post)
                name = ''

            message_list.flush((json_subpath / chunk.name).with_suffix('.json'))

    message_list.dump_stats()
