import re
from pathlib import Path


class QLIE:
    class Title:
        RE = re.compile(r'\^savetext,"(.*)"', re.IGNORECASE)
        def __init__(self, match):
            self.name = 'TITLE'
            self.text = match.group(1)

        def __str__(self):
            return f'^savetext,"{self.text}"'

    class Message:
        RE = re.compile(r'^【(.*?)】')


        def __init__(self, match, text):
            self.name = match.group(1)
            self.text = text
            self.text = self.text.replace('[n]', '\n')

        def __str__(self):
            self.text = self.text.replace('\n', '[n]')
            return f'【{self.name}】\n{self.text}'

    class Select:
        RE = re.compile(r'\^select,(.*)')
        def __init__(self, match):
            self.options = match.group(1).split(',')

        def __str__(self):
            return f'^select,{",".join(self.options)}'

    Text = Title | Message


    def __init__(self, lines):
        self.lines = lines


    @classmethod
    def read(cls, path: Path):
        text = path.read_text(encoding='utf-16')

        lines = []
        raw_lines = iter(text.splitlines(keepends=False))
        while True:
            _SENTINEL = object()
            line = next(raw_lines, _SENTINEL)
            if line is _SENTINEL:
                break

            if match := cls.Title.RE.match(line):
                lines.append(cls.Title(match))
            elif match := cls.Message.RE.match(line):
                lines.append(cls.Message(match, next(raw_lines)))
            elif match := cls.Select.RE.match(line):
                lines.append(cls.Select(match))
            else:
                lines.append(line)

        return cls(lines)


    def write(self, path: Path, newline='\r\n'):
        self.lines.append('')
        path.write_text(
            newline.join(str(line) for line in self.lines),
            encoding='utf-16'
        )
