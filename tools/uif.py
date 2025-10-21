import json
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parent
SPARE_CHARS = list('龠黼黻黹黥麑鬯髟驩馘隰醢')

class UIF:
    def __init__(self):
        with open(MODULE_PATH/'uif_dict.json') as f:
            self.dict = json.load(f)

        with open(MODULE_PATH/'uif_config.json') as f:
            self.conf = json.load(f)

    def replace(self, s):
        result = []
        for char in s:
            if char in self.dict:
                result.append(self.dict[char])
            else:
                try:
                    char.encode('cp932')
                    result.append(char)
                except UnicodeEncodeError:
                    spare = SPARE_CHARS.pop()
                    self.dict[char] = spare
                    result.append(spare)
        return ''.join(result)

    def gen_conf(self, path):
        self.conf['character_substitution']['source_characters'] = ''.join(self.dict.values())
        self.conf['character_substitution']['target_characters'] = ''.join(self.dict.keys())
        with open(path, 'w') as f:
            json.dump(self.conf, f, indent=2, ensure_ascii=False)
