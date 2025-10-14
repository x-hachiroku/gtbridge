import json
from pathlib import Path
from shutil import copyfile

from gtbridge import load
from gtbridge.games.tmr_hiro.srp import SRP

from extract import PLAYER_NAME


if __name__ == '__main__':
    with open('./names.json') as f:
        names = json.load(f)

    json_dir = Path('data/translated_json')
    original_srp_dir = Path('data/original_srp')
    out_dir = Path('data/srp')

    for original_srp in original_srp_dir.glob('*'):
        if original_srp.is_dir():
            continue

        relative = original_srp.relative_to(original_srp_dir)
        translated_json = json_dir / relative.with_suffix('.json')
        out_path = out_dir / relative.with_suffix('')
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if not translated_json.exists():
            copyfile(original_srp, out_path)
            continue

        srp = SRP(original_srp)

        translated_messages = load(translated_json)
        for message in translated_messages:
            message.message = message.message.replace(PLAYER_NAME, '＄α')

        translated_messages = iter(translated_messages)
        for entry in srp.entries:
            if not entry.text:
                continue

            message = next(translated_messages)
            assert ',' not in message.message, relative

            entry.text = message.message
            if entry.name:
                entry.name = names.get(entry.name, entry.name)

        _SENTINEL = object()
        assert next(translated_messages, _SENTINEL) is _SENTINEL, relative

        srp.write(out_path)
