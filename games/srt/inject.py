import pysrt
from pathlib import Path
from bs4 import BeautifulSoup

from gtbridge import load

for j in Path('./data/translated_json/').rglob('*.json'):
    relative_path = j.relative_to('./data/translated_json/')
    translated = load(j)

    srt = Path('./data/original_srt/') / relative_path.with_suffix('.srt')
    subs = pysrt.open(srt)
    for line in subs:
        message = translated.pop(0)
        assert line.text == message.original
        line.text = message.message

    output_path = Path('./data/translated_srt/') / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subs.save(output_path.with_suffix('.chs.srt'), encoding='utf-8')
