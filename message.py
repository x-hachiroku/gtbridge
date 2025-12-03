import os
import re
import json
from typing import List
from dataclasses import dataclass, asdict, field
from unicodedata import normalize

BRACKETS = {
    ('<', '>'), ('[', ']'), ('{', '}'),
    ('＜', '＞'), ('［', '］'), ('｛', '｝'),
    ('「', '」'), ('『', '』'),
    ('【', '】'), ('〖', '〗'),
    ('〔', '〕'),
}


PRE_NORM_PATTERNS = (
    re.compile(r'[\uFF61-\uFF9F]+'),
    re.compile(r'.[\u3099\u309A]'),
)

FW_POST_NORM_PATTERN = re.compile(r'[0-9A-Za-z]')
HW_POST_NORM_PATTERN = re.compile(r'[０-９Ａ-Ｚａ-ｚ]')


_VALID_JA_CHARS = r'\u3005\u3006\u3040-\u309F\u30A1-\u30FA\u30FC-\u30FF\u3400-\u4DBF\u4E00-\u9FFF'
VALID_JA_PATTERN = re.compile(r'[' + _VALID_JA_CHARS + r']')
_VALID_SYMBOLS = r'0-9A-Za-z０-９Ａ-Ｚａ-ｚ\(\)（）《》…、?？!！%％ー―〇'

_INVALID_CHARS_GROUP = r'([^' + _VALID_JA_CHARS + _VALID_SYMBOLS + r']*)'
MESSAGE_PATTERN = re.compile(
    r'\A' +
    _INVALID_CHARS_GROUP +
    r'(.*?)' +
    _INVALID_CHARS_GROUP +
    r'\Z',
    re.DOTALL
)

_BASE_REPL_TABLE = {
    r'[\.。]{3}':  '…' ,
    r'[\u2010-\u2015\u2500-\u257f\uFF0D]{1,2}': '——',
    r'[❶➀➊]': '1', r'[❷➁➋]': '2', r'[❸➂➌]': '3', r'[❹➃➍]': '4', r'[❺➄➎]': '5',
    r'[❻➅➏]': '6', r'[❼➆➐]': '7', r'[❽➇➑]': '8', r'[❾➈➒]': '9', r'[❿➉➓]': '10',
}

_PRE_REPL_TABLE = {
    r'[·˙·•․‧∙⋅⸱⸳⸳ꞏ]': '・',
}

HALFWIDTH_NEG_LOOKBEHIND = r'(?<![\x01-\x024F])'
_POST_REPL_TABLE = {
    HALFWIDTH_NEG_LOOKBEHIND + r'~':        '～',
    r'[・˙·•․‧∙⋅⸱⸳⸳ꞏ]': '·',
    r'([^'+_VALID_JA_CHARS+'])ー+': r'\1——',
}

_WIDTH_POST_REPL_TABLE = {
    HALFWIDTH_NEG_LOOKBEHIND + r'[.。] *':  '。',
    HALFWIDTH_NEG_LOOKBEHIND + r'[,﹐] *':  '，',
    HALFWIDTH_NEG_LOOKBEHIND + r'[!！] *':  '！',
    HALFWIDTH_NEG_LOOKBEHIND + r'[?？] *':  '？',
    HALFWIDTH_NEG_LOOKBEHIND + r' *& *':    '＆',
}

_GBK_REPL_TABLE = {
    r'[\u2600-\u27BF]':  '～',
    r'[\u25A0-\u25FF\u26AA-\u26AC\u2B00-\u2BFF\U0001F300-\U0001F5FF\U0001F780-\U0001F7FF]': '〇',
}


BASE_REPL_TABLE = { re.compile(k) : v for k, v in _BASE_REPL_TABLE.items() }
PRE_REPL_TABLE = { re.compile(k) : v for k, v in _PRE_REPL_TABLE.items() }
POST_REPL_TABLE = { re.compile(k) : v for k, v in _POST_REPL_TABLE.items() }
WIDTH_POST_REPL_TABLE = { re.compile(k) : v for k, v in _WIDTH_POST_REPL_TABLE.items() }
GBK_REPL_TABLE = { re.compile(k) : v for k, v in _GBK_REPL_TABLE.items() }
PRE_REPL_TABLE.update(BASE_REPL_TABLE)
POST_REPL_TABLE.update(BASE_REPL_TABLE)


@dataclass
class MessageEntity:
    name:      str = ''
    original:  str = ''
    message:   str = ''
    pre:       str = ''
    post:      str = ''
    tags:      List[str] = field(default_factory=list)


def preprocess(text):
    for pattern in PRE_NORM_PATTERNS:
        text = pattern.sub(lambda x: normalize('NFKC', x.group(0)), text)

    for pattern, repl in PRE_REPL_TABLE.items():
        text = pattern.sub(repl, text)

    return text


class MessageList:
    def __init__(self, gbk=False):
        self.messages = []
        self.message_count = 0
        self.char_conut = 0
        self.names = {}

        if gbk:
            PRE_REPL_TABLE.update(GBK_REPL_TABLE)

    def append(self, text, name='', original='', pre='', post='', tags=None):
        if original == '':
            original = pre+text+post
        if tags is None:
            tags = []

        _pre, content, _post = MESSAGE_PATTERN.search(preprocess(text)).groups()
        pre = pre + _pre
        post = _post + post

        for bracket in BRACKETS:
            if (bracket[0] in pre and (
                content.count(bracket[0]) < content.count(bracket[1])
                or content.find(bracket[0]) > content.find(bracket[1])
            )):
                pre, extra = pre.rsplit(bracket[0], 1)
                content = bracket[0] + extra + content

            if (bracket[1] in post and (
                content.count(bracket[0]) > content.count(bracket[1])
                or content.rfind(bracket[0]) > content.rfind(bracket[1])
            )):
                extra, post = post.split(bracket[1], 1)
                content = content +  extra + bracket[1]

            if content.count(bracket[0]) != content.count(bracket[1]):
                tags.append('BRACKETS')

        if not VALID_JA_PATTERN.search(content):
            self.messages.append(MessageEntity(
                name     = name,
                original = original,
                message  = '',
                pre      = pre + content,
                post     = post,
                tags     = tags,
            ))

        else:
            self.message_count += 1
            self.char_conut += len(content)
            self.messages.append(MessageEntity(
                name     = name,
                original = original,
                message  = '「' + content + '」', # so galtransl wont mess up quotes
                pre      = pre,
                post     = post,
                tags     = tags,
            ))

        if name:
            if name not in self.names:
                self.names[name] = 0
            self.names[name] += 1

    def flush(self, filename):
        count =  len(self.messages)
        if count > 0:
            with open(filename, 'w') as f:
                json.dump([asdict(x) for x in self.messages], f, ensure_ascii=False, indent=2)
            self.messages.clear()
        return count

    def dump_stats(self, filename=None):
        if filename:
            name_dict = {}
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    name_dict = json.load(f)

            for name in sorted(self.names, key=self.names.get, reverse=True):
                if name not in name_dict:
                    name_dict[name] = name

            with open(filename, 'w') as f:
                json.dump(name_dict, f, ensure_ascii=False, indent=2)

        print(f'{self.message_count} messages extracted, {self.char_conut} chars in total.')


def to_fullwidth(s: str) -> str:
    result = []
    for ch in s:
        code = ord(ch)
        if ch == ' ':
            result.append('\u3000')
        elif FW_POST_NORM_PATTERN.match(ch):
            result.append(chr(code + 0xFEE0))
        else:
            result.append(ch)
    return ''.join(result)

def load(filename, fullwidth=False, gbk=False):
    if fullwidth:
        POST_REPL_TABLE.update(WIDTH_POST_REPL_TABLE)

    if gbk:
        POST_REPL_TABLE.update(GBK_REPL_TABLE)

    with open(filename, 'r') as f:
        data = json.load(f)

    messages = []
    for i in data:
        if len(i['message']) > 0:
            assert i['message'][0] == '「' and i['message'][-1] == '」'
            i['message'] = i['message'][1:-1]

        if len(i['message']) > 0 and i['message'][-1] == '。':
                i['message'] = i['message'][:-1]

        message = i['message']

        if fullwidth:
            message = to_fullwidth(message)
        else:
            message = HW_POST_NORM_PATTERN.sub(lambda x: normalize('NFKC', x.group(0)), message)

        for pattern, repl in POST_REPL_TABLE.items():
            message = pattern.sub(repl, message)

        message = i['pre'] + message + i['post']

        messages.append(MessageEntity(
            name     = i['name'],
            original = i['original'],
            message  = message,
            pre      = '',
            post     = '',
            tags     = i['tags'],
        ))

    return messages
