import json
from glob import glob

for t in glob('./translated_json/**/*.json', recursive=True):
    o = t.replace('translated_json', 'original_json')

    with open(o, 'r') as f:
        original = json.load(f)
    with open(t, 'r') as f:
        translated = json.load(f)

    assert len(original) == len(translated), t

    for i in range(len(original)):
        translated[i]['original'] = original[i]['original']
        translated[i]['pre'] = original[i]['pre']
        translated[i]['post'] = original[i]['post']

    with open(t, 'w') as f:
        json.dump(translated, f, indent=2, ensure_ascii=False)
