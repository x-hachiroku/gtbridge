from pathlib import Path
from gtbridge import load
from gtbridge.tools.uif import UIF


translated_txt_path = Path('./data/translated_txt')
translated_txt_path.mkdir(exist_ok=True, parents=True)

uif = UIF()

for j in Path('./data/translated_json').glob('*.json'):
    lines = []
    messages = load(j)
    for message in messages:
        lines.append(message.original)
        lines.append(uif.replace(message.message))
        lines.append('')

    (translated_txt_path / j.name).with_suffix('.txt').write_text('\n'.join(lines))

uif.gen_conf('./data/uif_config.json')
