import re
from pathlib import Path
from gtbridge import MessageList

LINE_PATTERN = re.compile(r'^(?:@@)?[^@]*(?:@@)?\s*$', re.DOTALL | re.MULTILINE)

original_scenario_dir = Path('./data/original/AVG_HWA/scenario')
original_json_dir = Path('./data/original_json')
original_json_dir.mkdir(parents=True, exist_ok=True)


TITLE_PREFIX = 'cap'
LABEL_PREFIX = 'na_'

SKIP_PREFIX = (
    'BGM',
    'bg_',
    'ev_',
    'sl_',
    'fj_',
    'jj_',
    'quake_',
    'sd_',
    'se_',
    'st_',
    'flag_',
    'v1_',
    'v2_',
    'v3_',
)

NAME_DICT = {
    'n_iam':       ('俺', '俺'),
    'n_hero':      ('夏野', '夏野'),
    'n_himeko':    ('姫子', '姫子'),
    'n_yukiko':    ('雪子', '雪子'),
    'n_sakurako':  ('桜子', '樱子'),
    'n_aisaki':    ('愛咲', '愛咲'),
}

if __name__ == '__main__':
    message_list = MessageList()

    for txt in original_scenario_dir.glob('*.txt'):
        _text = txt.read_text(encoding='cp932')
        lines = LINE_PATTERN.findall(_text)
        leftover = LINE_PATTERN.split(_text)
        leftover = [l for l in leftover if l.strip()]
        if len(leftover) > 0:
            print(f'Leftover text in {txt}: {leftover}...')

        name = ''
        for line in lines:

            pre = ''
            post = ''

            line = line.strip()
            if not line:
                continue

            if line[:2] == '@@':
                pre = '@@'
                line = line[2:]
            if line[-2:] == '@@':
                post = '@@'
                line = line[:-2]

            if line.startswith(TITLE_PREFIX):
                message_list.append(
                    line[len(TITLE_PREFIX):],
                    name='TITLE',
                    pre=pre+TITLE_PREFIX,
                    post=post,
                )

            elif line.startswith(LABEL_PREFIX):
                line = line[len(LABEL_PREFIX):]
                assert (not line) or (line[:2] == '//' and line[-2:] == '//'), line
                name = line[2:-2].strip()
                if name.startswith('n_'):
                    name = NAME_DICT.get(name[0], (name[2:]))

            elif line.startswith(SKIP_PREFIX):
                continue

            else:
                message_list.append(
                    name=name,
                    text=line,
                    pre=pre,
                    post=post,
                )

        for message in message_list.messages:
            for _p, _n in NAME_DICT.items():
                message.message = message.message.replace(_p, _n[0])
            if '_' in message.message:
                print(f'Unmanaged underscore in message: {message.message}')

        message_list.flush(original_json_dir / (txt.name + '.json'))

    message_list.dump_stats('./names.json')
