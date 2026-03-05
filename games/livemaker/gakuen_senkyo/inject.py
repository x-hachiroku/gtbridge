import csv
import json
from pathlib import Path

from gtbridge import load
from gtbridge.tools.uif import UIF
from extract import parse_name


ORIGINAL_DATA_DIR = Path('./data/original_csv')
TRANSLATED_JSON_DIR = Path('./data/translated_json')
TRANSLATED_DATA_DIR = Path('./data/translated_csv')

uif = UIF()

with open('names.json') as f:
    NAMES = json.load(f)
# for name in list(NAMES.keys()):
#     NAMES[name] = uif.replace(NAMES[name])


def inject_file(csv_path: Path, json_path: Path, out_path: Path) -> None:
    messages = iter(load(str(json_path)))

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(csv_path, newline='') as f_in, \
         open(out_path, 'w', newline='') as f_out:

        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames, lineterminator='\r\n')
        writer.writeheader()

        for row in reader:
            original_text = row['Original text']
            row['Translated text'] = original_text
            if not original_text:
                writer.writerow(row)
                continue

            name, original_text = parse_name(original_text)

            if not original_text.strip():
                writer.writerow(row)
                continue

            msg = next(messages)
            assert name + msg.original == row['Original text']

            translated_text = '\n'.join( (NAMES.get(name, name), msg.message.lstrip('\n')) )

            row['Translated text'] = uif.replace(translated_text)
            writer.writerow(row)

        _SENTINEL = object()
        assert next(messages, _SENTINEL) is _SENTINEL


if __name__ == '__main__':
    for csv_path in ORIGINAL_DATA_DIR.rglob('*.csv'):
        rel = csv_path.relative_to(ORIGINAL_DATA_DIR)
        json_path = TRANSLATED_JSON_DIR / rel.with_suffix('.json')

        if not json_path.exists():
            print(f'Warning: No translation found for {csv_path}, skipping...')
            continue

        out_path = TRANSLATED_DATA_DIR / rel
        inject_file(csv_path, json_path, out_path)

    uif.gen_conf('./data/uif_config.json')
