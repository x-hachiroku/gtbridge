import json
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parent
SPARE_CHARS = list('龠黼黻黹黥麑鬯髟驩馘隰醢')

class UIF:
    def __init__(self):
        with open(MODULE_PATH/'uif_dict.json') as f:
            self.dict = json.load(f)
        self.dict_rev =  {v: k for k, v in self.dict.items()}
        self.duped = set()

        with open(MODULE_PATH/'uif_config.json') as f:
            self.conf = json.load(f)

    def replace(self, s):
        result = []
        for char in s:
            if char in self.dict_rev:
                self.duped.add(char)
                result.append(char)
                continue

            if char in self.dict:
                result.append(self.dict[char])
            else:
                try:
                    char.encode('cp932')
                    result.append(char)
                except UnicodeEncodeError:
                    print(f'Warning: {repr(char)} not in base dict or repeated. Allocating extra mapping.')
                    spare = SPARE_CHARS.pop()
                    self.dict[char] = spare
                    self.dict_rev[spare] = char
                    result.append(spare)
        return ''.join(result)

    def recover(self, s):
        result = []
        for char in s:
            if char in self.dict_rev:
                result.append(self.dict_rev[char])
            else:
                result.append(char)
        return ''.join(result)

    def gen_conf(self, path):
        if self.duped:
            print(f'Warning: replacer chars found: {self.duped}')

        self.conf['character_substitution']['source_characters'] = ''.join(self.dict.values())
        self.conf['character_substitution']['target_characters'] = ''.join(self.dict.keys())
        with open(path, 'w') as f:
            json.dump(self.conf, f, indent=2, ensure_ascii=False)
