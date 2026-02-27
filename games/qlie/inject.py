import re
import json
from pathlib import Path

from gtbridge import load
from gtbridge.games.qlie import QLIE

ORIGINAL_DATA_DIR = Path('./data/original_data')
TRANSLATED_JSON_DIR = Path('./data/translated_json')
TRANSLATED_DATA_DIR = Path('./data/translated_data')

RB_RE = re.compile(r'\[rb,(.*?),(.*?)\]')

with open('./names.json') as f:
    names = json.load(f)


def inject_file(s_path: Path, json_path: Path, out_path: Path) -> None:
    qlie = QLIE.read(s_path)
    messages = iter(load(str(json_path)))

    for line in qlie.lines:
        if isinstance(line, QLIE.Text):
            msg = next(messages)
            assert msg.original == line.text, (msg.original, line.text)
            _msg = RB_RE.sub('', msg.message)
            if '[' in _msg or ']' in _msg:
                print(f'Warning: Unmatched brackets in message: {msg.message}')
            line.text = msg.message
            line.name = names.get(line.name, line.name)

        elif isinstance(line, QLIE.Select):
            for i in range(len(line.options)):
                msg = next(messages)
                assert msg.original == line.options[i]
                line.options[i] = msg.message

    _SENTINEL = object()
    assert next(messages, _SENTINEL) is _SENTINEL

    out_path.parent.mkdir(parents=True, exist_ok=True)
    qlie.write(out_path)


if __name__ == '__main__':
    for s_path in ORIGINAL_DATA_DIR.rglob('*.s'):
        rel = s_path.relative_to(ORIGINAL_DATA_DIR)
        json_path = TRANSLATED_JSON_DIR / rel.with_suffix('.json')

        if not json_path.exists():
            print(f'Warning: No translation found for {s_path}, skipping...')
            continue

        out_path = TRANSLATED_DATA_DIR / rel
        inject_file(s_path, json_path, out_path)
