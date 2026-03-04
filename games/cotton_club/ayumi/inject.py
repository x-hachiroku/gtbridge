import json
from pathlib import Path

from gtbridge import load
from gtbridge.games.cotton_club.loc import LOC
from gtbridge.tools.uif import UIF

ORIGINAL_DATA_DIR = Path('./data/original_data')
TRANSLATED_JSON_DIR = Path('./data/translated_json')
TRANSLATED_DATA_DIR = Path('./data/translated_data')

uif = UIF()

with open('names.json') as f:
    NAMES = json.load(f)

for name in NAMES:
    NAMES[name] = uif.replace(NAMES[name])


def inject_file(loc_path: Path, json_path: Path, out_path: Path) -> None:
    loc = LOC.from_file(loc_path)
    messages = iter(load(str(json_path)))

    for seg in loc.segments:
        text = seg.get_text()
        if not text:
            continue

        lines = text.splitlines(keepends=True)
        translated_lines = []

        if text[0] == ':':
            name_line = lines[0]
            name = name_line[1:-1]
            translated_lines.append(':' + NAMES.get(name, name) + '\n')
            lines = lines[1:]

        for line in lines:
            if not line.strip() or line[0] in ('\x00', '['):
                translated_lines.append(line)
                continue
            msg = next(messages)
            assert msg.original == line, (msg.original, line)
            translated_lines.append(uif.replace(msg.message))

        seg.set_text(''.join(translated_lines))

    _SENTINEL = object()
    assert next(messages, _SENTINEL) is _SENTINEL

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(loc.encode())


if __name__ == '__main__':
    for loc_path in ORIGINAL_DATA_DIR.rglob('*.loc'):
        rel = loc_path.relative_to(ORIGINAL_DATA_DIR)
        json_path = TRANSLATED_JSON_DIR / rel.with_suffix('.json')

        if not json_path.exists():
            print(f'Warning: No translation found for {loc_path}, skipping...')
            continue

        out_path = TRANSLATED_DATA_DIR / rel
        inject_file(loc_path, json_path, out_path)

    uif.gen_conf('./data/uif_config.json')
