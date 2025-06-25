import re

_NAME_PATTERN = b'(?:\x14\x00([^\x00]+)\x00)?'
_MESSAGE_PREFIX = b'\x10\x00\x00\x00\x00\x00[\x00\x01]\x00\x00\x00'
MESSAGE_PREFIX_PATTERN = re.compile(_MESSAGE_PREFIX)
MESSAGE_PREFIX_LEN = 10
MESSAGE_PATTERN = re.compile(_NAME_PATTERN + _MESSAGE_PREFIX + b'(....)', re.DOTALL) # Name, Message index


_OPTIONS_PREFIX = b'\xB0\x00(.)\x00\x00\x00'
_OPTIONS_POSTFIX = b'\x00\xA9\x00.\x00\x00\x00'
OPTIONS_PATTERN = re.compile(_OPTIONS_PREFIX + b'(.*?)' + _OPTIONS_POSTFIX, re.DOTALL) # Options count, Options texts


_JUMP_PATTERNS = [
    b'\x00\xA0\x00(....)',
    b'\x00[\xA1\xA2]\x00..\x00\x00(....)', # flag index (?)
    b'\xA3\x00..\x01\x00\x05\x00\x00\x00(....)',
    b'\xA5\x00\x64\x00\x01\x00\x06\x00\x00\x00(....)',
]

for i in range(2,7):
    _JUMP_PATTERNS.append(b'\x00\xA9\x00' + i.to_bytes(1, 'little') + b'\x00\x00\x00' + b'(....)' * i)

JUMP_PATTERNS = [re.compile(pattern, re.DOTALL) for pattern in _JUMP_PATTERNS]
