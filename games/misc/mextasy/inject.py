import re
import json
from pathlib import Path
from gtbridge import load
from extract import LINE_PATTERN, TITLE_PREFIX, LABEL_PREFIX, SKIP_PREFIX, NAME_DICT

if __name__ == '__main__':
    original_scenario_dir = Path('./data/original/AVG_HWA/scenario')
    translated_json_dir = Path('./data/translated_json')
    translated_scenario_dir = Path('./data/translated/AVG_HWA/scenario')
    translated_scenario_dir.mkdir(parents=True, exist_ok=True)

    with open('./names.json') as f:
        names = json.load(f)

    for txt in original_scenario_dir.glob('*.txt'):
        data = [b'']

        messages = iter(load(translated_json_dir / (txt.name + '.json'), fullwidth=True))
        lines = LINE_PATTERN.findall(txt.read_text(encoding='cp932'))

        for line in lines:
            line = line.strip()
            original = line

            if not line:
                continue

            if line[:2] == '@@':
                line = line[2:]
            if line[-2:] == '@@':
                line = line[:-2]

            if line.startswith(TITLE_PREFIX):
                message = next(messages)
                assert message.original == original
                message.message = message.message.replace('\n', '\r\n')
                data.append(message.message.encode('cp936'))

            elif line.startswith(LABEL_PREFIX):
                line = line[len(LABEL_PREFIX):].strip()
                if line:
                    assert line[:2] == '//' and line[-2:] == '//'
                    name = line[2:-2].strip()
                    if not name.startswith('n_'):
                        name = names[name]
                        original = '@@' + LABEL_PREFIX + '//' + name + '//@@'
                data.append(original.encode('cp936'))

            elif line.startswith(SKIP_PREFIX):
                data.append(original.encode('cp932'))

            else:
                message = next(messages)
                assert message.original == original
                _message = message.message

                if _message[:2] == '@@':
                    _message = _message[2:]
                if _message[-2:] == '@@':
                    _message = _message[:-2]

                message.message = message.message.replace('\n', '\r\n')
                for _p, _n in NAME_DICT.items():
                    message.message = message.message.replace(_n[1], _p)
                data.append(message.message.encode('cp936'))

        data.append(b'')
        (translated_scenario_dir / txt.name).write_bytes(b'\r\n'.join(data))
