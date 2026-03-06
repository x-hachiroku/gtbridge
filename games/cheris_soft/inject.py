import json
from pathlib import Path

from txt import TXT
from charset_checker import CharsetChecker
from gtbridge import load
from gtbridge.tools.uif import UIF

ORIGINAL_DATA_DIR = Path('./data/original_data')
TRANSLATED_JSON_DIR = Path('./data/translated_json')
TRANSLATED_DATA_DIR = Path('./data/translated_data')

charset_checker = CharsetChecker(TRANSLATED_DATA_DIR / 'IMG')

uif = UIF()

with open('./names.json') as f:
    NAMES = json.load(f)


def inject_file(txt_path):
    rel = txt_path.relative_to(ORIGINAL_DATA_DIR)
    msg_json_path = TRANSLATED_JSON_DIR / rel.with_suffix('.txt.json')
    tag_json_path = TRANSLATED_JSON_DIR / rel.with_suffix('.tag.json')

    if not msg_json_path.exists() and not tag_json_path.exists():
        print(f'Warning: No translation found for {txt_path}, skipping...')
        return

    txt = TXT.from_path(txt_path)

    messages = iter(load(msg_json_path)) if msg_json_path.exists() else iter([])
    tags = iter(load(tag_json_path)) if tag_json_path.exists() else iter([])

    for seg in txt.segments:
        if isinstance(seg, TXT.TextSegment):
            for i, text in enumerate(seg.texts):
                if not text.strip():
                    continue

                msg = next(messages)
                assert msg.original == text, (msg.original, text)

                if msg.name:
                    msg.message = '\n'.join(( NAMES[msg.name], msg.message ))

                seg.texts[i] = uif.replace(msg.message)
                charset_checker.add_string(seg.texts[i])

        elif isinstance(seg, TXT.TagSegment):
            for i, text in enumerate(seg.texts):
                if not text.strip():
                    continue
                tag_msg = next(tags)
                assert tag_msg.original == text
                seg.texts[i] = uif.replace(tag_msg.message)
                charset_checker.add_string(seg.texts[i])

    _SENTINEL = object()
    assert next(messages, _SENTINEL) is _SENTINEL
    assert next(tags, _SENTINEL) is _SENTINEL

    out_path = TRANSLATED_DATA_DIR / rel
    out_path.parent.mkdir(parents=True, exist_ok=True)
    txt.to_path(out_path)


if __name__ == '__main__':
    for txt_path in ORIGINAL_DATA_DIR.rglob('*.txt'):
        if txt_path.parts[2] == 'IMG':
            continue

        inject_file(txt_path)

    charset_checker.check()
