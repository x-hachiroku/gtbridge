import re
from pathlib import Path

TAG_TEXT_PATTERN = re.compile(r'"([^"]*)"')
RUBY_PATTERN = re.compile(r'<RUBY text\s*=\s*"[^"]*" target\s*=\s*"([^"]*)"\s*>')
SEGMENT_PATTERN = re.compile(r'(//.*?$|<[^>]*>\n?|^\s+^)', re.MULTILINE)

class TXT:
    class Segment:
        def __init__(self, raw):
            self.raw = raw
            self.texts = []

        def serialize(self):
            return self.raw

    class TagSegment(Segment):
        def __init__(self, raw):
            super().__init__(raw)
            self.texts = TAG_TEXT_PATTERN.findall(raw)
            # self.texts = [s.replace('\\n', '\n') for s in TAG_TEXT_PATTERN.findall(raw)]

        def serialize(self):
            texts_iter = iter(self.texts)
            def replace_cb(_):
                return '"' + next(texts_iter) + '"'
            return TAG_TEXT_PATTERN.sub(replace_cb, self.raw)

    class TextSegment(Segment):
        def __init__(self, raw):
            super().__init__(raw)
            self.texts = raw.split('\\w\\c')

        def serialize(self):
            return '\\w\\c'.join(self.texts)


    def __init__(self, segments):
        self.segments = segments

    def serialize(self):
        return ''.join(seg.serialize() for seg in self.segments)

    @classmethod
    def from_string(cls, s):
        s = RUBY_PATTERN.sub(r'\1', s)

        segments = []
        _segments = SEGMENT_PATTERN.split(s)
        for seg in _segments:
            if not seg:
                continue
            if not seg.strip() or seg[0:2] == '//':
                segments.append(TXT.Segment(seg))
            elif seg[0] == '<':
                segments.append(TXT.TagSegment(seg))
            else:
                segments.append(TXT.TextSegment(seg))

        return cls(segments)

    @classmethod
    def from_path(cls, p):
        p = Path(p)
        return cls.from_string(p.read_text(encoding='cp932'))

    def to_path(self, p):
        p = Path(p)
        p.write_text(self.serialize(), encoding='cp932', newline='\r\n')


if __name__ == "__main__":
    import sys

    file_path = sys.argv[1]

    with open(file_path, encoding='cp932') as f:
        original_data = f.read()

    txt = TXT.from_string(original_data)
    for i, seg in enumerate(txt.segments):
        print('Segment', i)
        print(repr(seg.raw))
        print()
    serialized_data = txt.serialize()

    assert original_data == serialized_data
