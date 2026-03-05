import re
import csv
from pathlib import Path

from gtbridge import MessageList


ORIGINAL_DATA_DIR = Path('./data/original_csv')
ORIGINAL_JSON_DIR = Path('./data/original_json')

ACTOR_PATTERN = re.compile(r'\A(.*?)(\s*[（「『].*)', re.DOTALL)

BRACKETS = {
    '（': '）',
    '「': '」',
    '『': '』',
}

def parse_name(text):
    name = ''
    if match := ACTOR_PATTERN.search(text):
        _text = match.group(2).strip()
        if BRACKETS[_text[0]] == _text[-1]:
            name = match.group(1)
            text = match.group(2)

    return name, text

def extract_file(csv_path: Path, message_list: MessageList) -> int:
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get('Original text', '')
            if not text:
                continue

            name, text = parse_name(text)

            if not text.strip():
                continue
            message_list.append(text, name=name)

    rel = csv_path.relative_to(ORIGINAL_DATA_DIR)
    out_path = ORIGINAL_JSON_DIR / rel.with_suffix('.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    return message_list.flush(out_path)


if __name__ == '__main__':
    message_list = MessageList()

    for csv_path in ORIGINAL_DATA_DIR.rglob('*.csv'):
        extract_file(csv_path, message_list)

    message_list.dump_stats('./names.json')
