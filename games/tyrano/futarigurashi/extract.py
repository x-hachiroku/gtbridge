import re
from pathlib import Path

from gtbridge import MessageList

MSG_PATTERN = re.compile(r'^(.*?)((?:\[\w\])*)$')

SCRIPT_START_PATTERN = re.compile(r'\[\s*iscript')
SCRIPT_END_PATTERN = re.compile(r'\[\s*endscript')
HTML_START_PATTERN = re.compile(r'\[\s*html')
HTML_END_PATTERN = re.compile(r'\[\s*endhtml')

CHATTAKL_PATTERN = re.compile(r'(\[\s*chat_talk .*?name="(.*?)".*text=")(.*?)("[^\]]*\])')
TIPS_PATTERN = re.compile(r'\[showTips subject="(.*)" text="(.*)"\]')
EVAL_PATTERNS = (
    re.compile(r'(\[\s*eval\s*exp="tf\.text\d*\s*\+?=\s*\')(.*?)(\'[^\]]*\])'),
    re.compile(r'(\[\s*eval\s*exp="f\.tipsText\s*\+?=\s*\')(.*?)(\'[^\]]*\])'),
    re.compile(r'(\[\s*glink.*?text=")(.*?)("[^\]]*\])'),
    re.compile(r'(\[\s*ptext.*?text=")(.*?)("[^\]]*\])'),
)

DIARY_PATTERN = re.compile(r"(\s*ID\d+.*text:')(.*?)('}.*)")


scenario_dir = Path('./data/app/data/scenario')
original_json_dir = Path('./data/original_json')
original_json_dir.mkdir(parents=True, exist_ok=True)


message_list = MessageList()

for ks in scenario_dir.rglob('*.ks'):
    ks_relative = original_json_dir / ks.relative_to(scenario_dir)
    ks_relative.parent.mkdir(parents=True, exist_ok=True)

    with open(ks, 'r') as f:
            lines = f.read().splitlines()

    i = 0
    name = ''
    msg = ''
    post = ''
    linerange = []
    while i < len(lines):
        line = lines[i].strip()
        if not line.strip():
            i+=1
            continue

        if msg and (line[0] in {'[', '@', ';', '*', '#'} or '[p]' in post or '[l]' in post):
            linerange.append(i)
            message_list.append(
                msg,
                name=name,
                post=post,
                tags=linerange,
            )
            name = ''
            msg = ''
            post = ''
            linerange = []


        if line[0]  == '[':
            if SCRIPT_START_PATTERN.match(line):
                while not SCRIPT_END_PATTERN.search(lines[i]):
                    i += 1

            elif HTML_START_PATTERN.match(line):
                while not HTML_END_PATTERN.search(lines[i]) :
                    i += 1

            elif match := CHATTAKL_PATTERN.match(line):
                _name = match.group(2)
                if _name == '自分':
                    _name = '先生'
                message_list.append(
                    match.group(3).replace('<br>', ''),
                    name=_name,
                    original=match.group(0),
                    pre=match.group(1),
                    post=match.group(4),
                )

            elif match := TIPS_PATTERN.match(line):
                _original = match.group(1) + '\n' + match.group(2)
                _msg = _original.replace('<br>', '')
                _msg = _msg.replace('　', '')
                message_list.append(
                    _msg,
                    name='TIPS',
                    tags=['TIPS'],
                    original=_original
                )

            else:
                for pattern in EVAL_PATTERNS:
                    if match := pattern.match(line):
                        if 'glink' in line:
                            _name = '選択肢'
                        else:
                            _name = 'SYSTEM'
                        message_list.append(
                            match.group(2).replace('<br>', ''),
                            name=_name,
                            original=match.group(0),
                            pre=match.group(1),
                            post=match.group(3),
                        )

        elif line.startswith('#'):
            name = line[1:].strip()

        elif line[0] not in {'@', ';', '*'}:
            if not linerange:
                linerange.append(i)
            match = MSG_PATTERN.match(line)
            msg += match.group(1).strip()
            post = match.group(2)

        i += 1


    count = message_list.flush(str(ks_relative) + '.json')
    if count == 0:
        print(f'{ks}: No message found.')


with open("./data/diary") as f:
    lines = f.read().splitlines()

for line in lines:
    match = DIARY_PATTERN.match(line)
    message_list.append(
        match.group(2).strip(),
        name='みお',
        original=line,
        pre=match.group(1),
        post=match.group(3),
    )

message_list.flush('./data/original_json/macro_init.ks.json')

message_list.dump_stats()
