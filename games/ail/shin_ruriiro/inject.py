import json
from shutil import copyfile
from pathlib import Path

from gtbridge import load
from gtbridge.tools.uif import UIF
from gtbridge.games.ail.sall_2006 import SALL
from extract import get_name


original_sall_dir = Path('./data/original')
translated_sall_dir = Path('./data/translated')
translated_json_dir = Path('./data/translated_json')
translated_sall_dir.mkdir(parents=True, exist_ok=True)

uif = UIF()

with open('./names.json') as f:
    names = json.load(f)
    for k, v in names.items():
        names[k] = uif.replace(v)

for original_sall_path in original_sall_dir.glob('*'):
    sall = SALL(original_sall_path.read_bytes())
    translated_json_path = translated_json_dir / original_sall_path.with_suffix('.json').name
    translated_sall_path = translated_sall_dir / original_sall_path.name
    if not translated_json_path.exists():
        copyfile(original_sall_path, translated_sall_path)
        print(f'Warning: {original_sall_path}: no translation found.')
        continue

    translated_messages = load(translated_json_path, fullwidth=True)
    for message in translated_messages:
        message.message = uif.replace(message.message)
    translated_messages = iter(translated_messages)

    for page in sall.pages:
        texts = page.get_texts()
        if not texts:
            continue

        new_texts = []

        if name := get_name(texts[0]):
            new_texts.append(f'【{names.get(name, name)}】')
            texts.pop(0)

        if not texts:
            continue

        name_inside = any(get_name(t) for t in texts)

        if len(texts) > 3 or name_inside:
            for text in texts:
                if name := get_name(text):
                    new_texts.append(f'【{names.get(name, name)}】')
                else:
                    message = next(translated_messages)
                    assert text == message.original
                    new_texts.append(message.message.replace('\n', ''))
        else:
            message = next(translated_messages)
            assert '\n'.join(texts) == message.original
            new_texts.extend(message.message.split('\n'))

        page.set_texts(new_texts)

    _SENTINEL = object()
    assert next(translated_messages, _SENTINEL) is _SENTINEL

    translated_sall_path.write_bytes(sall.to_bytes())

uif.gen_conf('./data/uif_config.json')
