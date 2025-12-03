import re
import itertools
from pathlib import Path

from gtbridge import MessageList

TAG_PATTERN = re.compile(r'(\[.*?\]|f\.\w+)')
MESSAGE_PATTERN = re.compile(
    r'(?P<pre>\[tb_start_text\s+[^\]]*\].*?\n'
    r'(?:#(?P<name>.*?)\s*\n)?)'
    r'(?P<text>.*?)'
    r'(?P<post>(?:\[[^\]]*\])*?\s*)'
    r'(?=\n\[|\[_tb_end_text\])',
    re.DOTALL | re.MULTILINE
)
PTEXT_PATTERN = re.compile(r'(?P<pre>\[ptext(?=\s).*text\s*=\s*")(?P<text>.*?)(?P<post>\".*\])')
EVAL_TEXT_PATTERN = re.compile(r'(?P<pre>\[eval exp=".*?=)(?P<text>.*?)(?P<post>"\])')
CONDITION_TEXT_PATTERN = re.compile(r'(?P<pre>message: ")(?P<text>.*?)(?P<post>",)')
MESSAGE_LIST_PATTERN = re.compile(r'\[eval exp="f.lines = \[(.*?)\]\[f.random_num.? - 1\]"\]')

json_dir = Path('./data/original_json')
scenario_dir = Path('./data/original/data/scenario')


if __name__ == '__main__':
    message_list = MessageList()
    for ks in scenario_dir.rglob('*.ks'):
        ks_relative = ks.relative_to(scenario_dir)
        json_path = json_dir / ks_relative.with_suffix('.json')
        json_path.parent.mkdir(parents=True, exist_ok=True)

        with open(ks, 'r') as f:
            script = f.read()

        for match in itertools.chain(
            MESSAGE_PATTERN.finditer(script),
            PTEXT_PATTERN.finditer(script),
            EVAL_TEXT_PATTERN.finditer(script),
            CONDITION_TEXT_PATTERN.finditer(script),
        ):
            pre = match.group('pre')
            name = match.groupdict().get('name') or ''
            text = match.group('text')
            post = match.group('post') or ''
            text = text.replace('[r]', '')
            text = text.replace('\n', '')
            tags = []
            for _match in TAG_PATTERN.finditer(text):
                tags.append('TAG:' + _match.group(0))
            message_list.append(
                original = match.group(0),
                pre = pre,
                name = name,
                text = text,
                post = post,
                tags = tags,
            )

        count = message_list.flush(json_path)

        for i, match in enumerate(MESSAGE_LIST_PATTERN.finditer(script)):
            messages = match.group(1).split(', ')
            for message in messages:
                message = message.strip("'")
                message_list.append(message)
            count += message_list.flush(json_path.with_suffix(f'.message_list_{i:02d}.json'))

        if count == 0:
            print(f'{ks}: No message found.')

    message_list.dump_stats('./names.json')
