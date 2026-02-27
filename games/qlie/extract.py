import re
from pathlib import Path

from gtbridge import MessageList
from gtbridge.games.qlie import QLIE

ORIGINAL_DATA_DIR = Path('./data/original_data')
ORIGINAL_JSON_DIR = Path('./data/original_json')


RUBY_RE = re.compile(r'\[rb,(.*?),(.*?)\]')

def ruby_cb(match):
    return match.group(1)


def extract_file(s_path: Path, message_list: MessageList) -> int:
    qlie = QLIE.read(s_path)

    for line in qlie.lines:
        if isinstance(line, QLIE.Text):
            tags = None
            text = line.text
            if isinstance(line, QLIE.Message):
                ruby_matches = RUBY_RE.finditer(text)
                for m in ruby_matches:
                    if '・' in m.group(2):
                        tags = ['RUBY']
                    else:
                        print('Warning: Skipping ruby', m.group(1), m.group(2))
                text = RUBY_RE.sub(ruby_cb, text)
            message_list.append(text, original=line.text, name=line.name, tags=tags)

        elif isinstance(line, QLIE.Select):
            for opt in line.options:
                message_list.append(opt, name='SELECT')

    rel = s_path.relative_to(ORIGINAL_DATA_DIR)
    out_path = ORIGINAL_JSON_DIR / rel.with_suffix('.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    return message_list.flush(out_path)


if __name__ == '__main__':
    message_list = MessageList()

    for s_path in ORIGINAL_DATA_DIR.rglob('*.s'):
        extract_file(s_path, message_list)

    message_list.dump_stats('./names.json')
