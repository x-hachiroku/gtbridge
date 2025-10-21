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

POST_NORM_PATTERN = re.compile(r'[０-９Ａ-Ｚａ-ｚ]')


_VALID_JA_CHARS = r'\u3040-\u309F\u30A0-\u30FF\u3400-\u4DBF\u4E00-\u9FFF'
VALID_JA_PATTERN = re.compile(r'[' + _VALID_JA_CHARS + r']')
_VALID_SYMBOLS = r'0-9A-Za-z０-９Ａ-Ｚａ-ｚ\(\)（）《》…、？！ー―〇'

_INVALID_CHARS_GROUP = r'([^' + _VALID_JA_CHARS + _VALID_SYMBOLS + r']*)'
MESSAGE_PATTERN = re.compile(
    r'\A' +
    _INVALID_CHARS_GROUP +
    r'(.*?)' +
    _INVALID_CHARS_GROUP +
    r'\Z',
    re.DOTALL
)

BASE_REPL_TABLE = {
    r'[\.。]{3}':  '…' ,
    r'[\u2600-\u27BF]':  '～',
    r'[\u2010-\u2015\u2500-\u257f\uFF0D]{1,2}': '——',
    r'[\u25A0-\u25FF\u26AA-\u26AC\u2B00-\u2BFF\U0001F300-\U0001F5FF\U0001F780-\U0001F7FF]': '〇',
    r'[❶➀➊]': '1', r'[❷➁➋]': '2', r'[❸➂➌]': '3', r'[❹➃➍]': '4', r'[❺➄➎]': '5',
    r'[❻➅➏]': '6', r'[❼➆➐]': '7', r'[❽➇➑]': '8', r'[❾➈➒]': '9', r'[❿➉➓]': '10',
}

PRE_REPL_TABLE = {
    r'[·˙·•․‧∙⋅⸱⸳⸳ꞏ]': '・',
}

HALFWIDTH_NEG_LOOKBEHIND = r'(?<![\x01-\x024F])'
POST_REPL_TABLE = {
    # HALFWIDTH_NEG_LOOKBEHIND + r'[.。] *':  '。',
    HALFWIDTH_NEG_LOOKBEHIND + r'[,﹐] *':  '，',
    HALFWIDTH_NEG_LOOKBEHIND + r'[!！] *':  '！',
    HALFWIDTH_NEG_LOOKBEHIND + r'[?？] *':  '？',
    HALFWIDTH_NEG_LOOKBEHIND + r' *& *':    '＆',
    HALFWIDTH_NEG_LOOKBEHIND + r'~':        '～',
    r'[・˙·•․‧∙⋅⸱⸳⸳ꞏ]': '·',
    r'([^'+_VALID_JA_CHARS+'])ー+': r'\1——',
}

BASE_REPL_TABLE = { re.compile(k) : v for k, v in BASE_REPL_TABLE.items() }
PRE_REPL_TABLE = { re.compile(k) : v for k, v in PRE_REPL_TABLE.items() }
POST_REPL_TABLE = { re.compile(k) : v for k, v in POST_REPL_TABLE.items() }
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
    def __init__(self):
        self.messages = []
        self.message_count = 0
        self.char_conut = 0
        self.names = {}

    def append(self, text, name='', original='', pre='', post='', tags=None):
        if original == '':
            original = pre+text+post
        if tags is None:
            tags = []

        _pre, content, _post = MESSAGE_PATTERN.search(preprocess(text)).groups()
        pre = pre + _pre
        post = _post + post

        for bracket in BRACKETS:
            if content.count(bracket[0]) < content.count(bracket[1]) and pre.count(bracket[0]) > 0:
                pre, extra = pre.split(bracket[0], 1)
                content = bracket[0] + extra + content
            elif content.count(bracket[0]) > content.count(bracket[1]) and post.count(bracket[1]) > 0:
                extra, post = post.split(bracket[1], 1)
                content = content +  extra + bracket[1]
            if content.count(bracket[0]) != content.count(bracket[1]):
                tags.append('brackets')

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

            if name:
                if name not in self.names:
                    self.names[name] = 0
                self.names[name] += 1

            self.messages.append(MessageEntity(
                name     = name,
                original = original,
                message  = content,
                pre      = pre,
                post     = post,
                tags     = tags,
            ))

    def flush(self, filename):
        count =  len(list(filter(lambda x: x.message, self.messages)))
        if count > 0:
            with open(filename, 'w') as f:
                json.dump([asdict(x) for x in self.messages], f, ensure_ascii=False, indent=2)
        self.messages = []
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


def postprocess(text):
    text = POST_NORM_PATTERN.sub(lambda x: normalize('NFKC', x.group(0)), text)

    for pattern, repl in POST_REPL_TABLE.items():
        text = pattern.sub(repl, text)
    return text

def load(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    messages = []
    for i in data:
        if len(i['message']) > 0:
            if i['message'][-1] == '。':
                i['message'] = i['message'][:-1]
        if len(i['message']) > 0:
            if i['message'][0] == '「' and i['message'][-1] == '」':
                i['message'] = i['message'][1:-1]

        messages.append(MessageEntity(
            name     = i['name'],
            original = i['original'],
            message  = postprocess(i['pre']+i['message']+i['post']),
            pre      = '',
            post     = '',
            tags     = i['tags'],
        ))

    return messages
