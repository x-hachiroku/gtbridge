import json
import shutil
from pathlib import Path
from gtbridge.message import load
from gtbridge.tools.uif import UIF
from gtbridge.tools.replacer import Replacer

ORIGINAL_DATA_DIR = Path('./data/original_data')
TRANSLATED_DATA_DIR = Path('./data/translated_data')

uif = UIF()

tr = {}

for tag_json in Path('./data/translated_json/').rglob('*.tag.json'):
    data = load(tag_json)
    for entry in data:
        src = entry.original
        dst = entry.message

        if src in tr:
            if dst != tr[src]:
                print('Warn:', src, repr(dst), repr(tr[src]), dst==tr[src], sep='\n')
        else:
            tr[src] = dst

replacer = Replacer(tr)


def new_name(old_path, rel):
    rel = str(rel)
    _rel = rel
    rel = replacer.replace(rel)
    rel = uif.replace(rel)
    if rel != _rel:
        new_path = TRANSLATED_DATA_DIR / rel
        new_path.parent.mkdir(parents=True, exist_ok=True)
        print(old_path, '->', new_path)
        shutil.copy2(old_path, new_path)


for old_path in (list(ORIGINAL_DATA_DIR.rglob('*.tga'))):
    rel = old_path.relative_to(ORIGINAL_DATA_DIR)
    new_name(old_path, rel)

for old_path in (list(TRANSLATED_DATA_DIR.rglob('*.txt'))):
    rel = old_path.relative_to(TRANSLATED_DATA_DIR)
    new_name(old_path, rel)
