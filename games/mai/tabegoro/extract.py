import json
from pathlib import Path

from gtbridge import MessageList
from gtbridge.games.mai.sct import SCT

SCT_DICT = {
    'main.sct': (0x51D96, 0x5383F),
    'scene.sct': (0x51D96, 0x528EF),
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
                if message and message[0] == '＜' and message[-1] == '＞':
                    name = message[1:-1]
                    continue

                if len(message) >= 2 and message[-2] == '#':
                    post = message[-2:]
                    message = message[:-2]
                else:
                    post = ''

                if '#' in message:
                    print(f'Warning: unresolved control code in message: {message}')

                message_list.append(message, name=name, post=post)
                name = ''

            message_list.flush((json_subpath / chunk.name).with_suffix('.json'))

    message_list.dump_stats('names.json')
