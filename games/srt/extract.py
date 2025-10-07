import pysrt
from pathlib import Path
from bs4 import BeautifulSoup

from gtbridge import MessageList


message_list = MessageList()

for srt in Path('./data/original_srt/').rglob('*.srt'):
    relative_path = srt.relative_to('./data/original_srt/')
    for line in pysrt.open(srt):
        text = BeautifulSoup(line.text, 'lxml').get_text()
        parts = line.text.split(text)
        if len(parts) == 2:
            message_list.append(
                original=line.text,
                text=text.replace('\n', ' ').strip(),
                pre=parts[0],
                post=parts[1],
            )
        else:
            message_list.append(
                original=line.text,
                text=text.replace('\n', ' ').strip(),
                tags=['COMPLEX_FORMAT'],
            )

    output_path = Path('./data/original_json/') / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    message_list.flush(output_path.with_suffix('.json'))

message_list.dump_stats()
