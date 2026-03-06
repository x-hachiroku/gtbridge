import sys
from pathlib import Path

class CharsetChecker:
    def __init__(self, img_dir: Path):
        self.available_chars = None
        self.used_chars = set()

        for txt_file in img_dir.glob('*.txt'):
            with open(txt_file, 'rb') as f:
                blob = f.read()

            current_chars = set()
            ptr = blob.find(b'.tga') + 8

            while ptr + 28 <= len(blob):
                byte_data = blob[ptr:ptr+28]
                char = byte_data[1::-1].strip(b'\x00').decode('cp932')
                current_chars.add(char)
                ptr += 28

            if self.available_chars is None:
                self.available_chars = current_chars
            else:
                self.available_chars.intersection_update(current_chars)

        if self.available_chars is None:
            self.available_chars = set()

    def add_string(self, s: str):
        self.used_chars.update(s)

    def check(self):
        missing = self.used_chars - self.available_chars
        if missing:
            print(f"Warning: The following characters are used but not in the font intersection: {sorted(list(missing))}", file=sys.stderr)
