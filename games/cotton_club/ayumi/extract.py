import re
from pathlib import Path

from gtbridge import MessageList
from gtbridge.games.cotton_club.loc import LOC

ORIGINAL_DATA_DIR = Path('./data/original_data')
ORIGINAL_JSON_DIR = Path('./data/original_json')


def extract_file(loc_path: Path, message_list: MessageList) -> int:
    loc = LOC.from_file(loc_path)

    for seg in loc.segments:
        if text := seg.get_text():
            name = ''
            lines = text.splitlines(keepends=True)
            if text[0] == ':':
                name = lines[0][1:-1]
                lines = lines[1:]
            for line in lines:
                if not line.strip() or line[0] in ('\u0000', '['):
                    continue
                message_list.append(line, name=name)

    rel = loc_path.relative_to(ORIGINAL_DATA_DIR)
    out_path = ORIGINAL_JSON_DIR / rel.with_suffix('.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    return message_list.flush(out_path)


if __name__ == '__main__':
    message_list = MessageList()

    for loc_path in ORIGINAL_DATA_DIR.rglob('*.loc'):
        extract_file(loc_path, message_list)

    message_list.dump_stats('./names.json')
