import json
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parent
SPARE_CHARS = list('龠黼黻黹黥麑鬯髟驩馘隰醢')

class UIF:
    def __init__(self):
        with open(MODULE_PATH/'uif_dict.json') as f:
            self.base_dict = json.load(f)
            self.base_dict_rev = {v: k for k, v in self.base_dict.items()}
            self.dict = {}
            self.used_replacer = set()
            self.duped = set()

        with open(MODULE_PATH/'uif_config.json') as f:
            self.conf = json.load(f)

    def replace(self, s):
        result = []
        for char in s:
            if char in self.base_dict:
                self.dict[char] = self.base_dict[char]
                self.used_replacer.add(self.base_dict[char])
                del self.base_dict_rev[self.base_dict[char]]
                del self.base_dict[char]
            elif char in self.base_dict_rev:
                del self.base_dict[self.base_dict_rev[char]]
                del self.base_dict_rev[char]
            elif char in self.used_replacer:
                self.duped.add(char)
                result.append(char)

            if char in self.dict:
                result.append(self.dict[char])
            else:
                try:
                    char.encode('cp932')
                    result.append(char)
                except UnicodeEncodeError:
                    spare = SPARE_CHARS.pop()
                    self.dict[char] = spare
                    self.used_replacer.add(spare)
                    result.append(spare)
        return ''.join(result)

    def gen_conf(self, path):
        if self.duped:
            print(f'Warning: replacer chars found: {self.duped}')

        self.conf['character_substitution']['source_characters'] = ''.join(self.dict.values())
        self.conf['character_substitution']['target_characters'] = ''.join(self.dict.keys())
        with open(path, 'w') as f:
            json.dump(self.conf, f, indent=2, ensure_ascii=False)
