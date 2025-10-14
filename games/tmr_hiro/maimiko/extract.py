from pathlib import Path

from gtbridge import MessageList
from gtbridge.games.tmr_hiro.srp import SRP

message_list = MessageList()

original_path = Path('data/original_srp/')
original_json_path = Path('data/original_json/')

PLAYER_NAME = '智也'


if __name__ == '__main__':
    for file in original_path.glob('*'):
        if file.is_dir():
            continue
        srp = SRP(file)

        for entry in srp.entries:
            text = ''
            name = ''
            pre = ''
            original = ''

            if not entry.text:
                continue

            name = entry.name
            text = entry.text

            tags = []
            name = name.replace('＄α', PLAYER_NAME)
            if '＄α' in text:
                text = text.replace('＄α', PLAYER_NAME)
                tags.append('PLAYER_NAME_REPLACED')

            message_list.append(text, name, original=original, tags=tags, pre=pre)

        relative_path = file.relative_to(original_path)
        output_path = original_json_path / relative_path.with_suffix('.json')
        output_path.parent.mkdir(parents=True, exist_ok=True)

        message_list.flush(output_path)

    message_list.dump_stats('./names.json')
