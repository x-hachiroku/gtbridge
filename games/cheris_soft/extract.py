import json
from pathlib import Path

from txt import TXT
from gtbridge import MessageList

ORIGINAL_DATA_DIR = Path('./data/original_data')
ORIGINAL_JSON_DIR = Path('./data/original_json')


def extract_file(txt_path, msg_list, tag_list):
    if txt_path.parts[2] == 'IMG':
        return

    txt = TXT.from_path(txt_path)
    rel = txt_path.relative_to(ORIGINAL_DATA_DIR)

    for seg in txt.segments:
        if isinstance(seg, TXT.TextSegment):
            for text in seg.texts:
                if not text.strip():
                    continue

                lines = text.split('\n')
                name = ''
                if len(lines) > 1 and lines[1].startswith('「'):
                    name = lines[0]
                    lines = lines[1:]
                msg_list.append('\n'.join(lines), name=name, original=text)

        elif isinstance(seg, TXT.TagSegment):
            for text in seg.texts:
                if not text.strip():
                    continue
                tag_list.append(text)


    out_msg_path = ORIGINAL_JSON_DIR / rel.with_suffix('.txt.json')
    out_msg_path.parent.mkdir(parents=True, exist_ok=True)
    msg_list.flush(out_msg_path)

    out_tag_path = ORIGINAL_JSON_DIR / rel.with_suffix('.tag.json')
    out_tag_path.parent.mkdir(parents=True, exist_ok=True)
    tag_list.flush(out_tag_path)


if __name__ == '__main__':
    msg_list = MessageList()
    tag_list = MessageList()

    for txt_path in ORIGINAL_DATA_DIR.rglob('*.txt'):
        extract_file(txt_path, msg_list, tag_list)

    msg_list.dump_stats('./names.json')
