from pyparsing import (
    Word,
    Suppress,
    QuotedString,
    Combine,
    Group,
    ZeroOrMore,
    Dict,
    unicode,
)
printables = unicode.printables

element_start = Suppress('[') + Word(printables, exclude_chars=' ]')('tag')
element_end = Suppress(']')

attr_name = Word(printables, exclude_chars=' =')
attr_value = Combine(
    QuotedString('"') | QuotedString("'") | Word(printables, exclude_chars=' []')
    + ZeroOrMore(QuotedString('[', end_quote_char=']', unquote_results=False))
)
attribute = Group((attr_name + Suppress('=') + attr_value) | Word('*'))
attributes = Dict(ZeroOrMore(attribute))

element = element_start + attributes + element_end

script = Suppress('@') + Word(printables, exclude_chars=' ')('tag') + attributes

def parse_line(line):
    line = line.strip()
    if not line:
        return {}

    try:
        match line[0]:
            case '[':
                pattern = element
            case '@':
                pattern = script
            case _:
                return {}

        return pattern.parseString(line).asDict()
    except Exception:
        print(f"Failed to parse line: {line}")
        return {}


def construct_tag(parsed):
    if 'tag' not in parsed:
        return ''

    line = f"[{parsed['tag']}"
    for key, value in parsed.items():
        if key != 'tag':
            line += f' {key}="{value}"'
    line += ']'
    return line


if __name__ == "__main__":
    for sample in (
        '[button name="ch,ch_25" fix="true" target="*ch_speed_change" graphic="&tf.btn_path_off" x="&tf.config_x[6]" y="355" exp="tf.set_ch_speed = 25; tf.config_num_ch = 5"]',
        '[glink storage="link.ks" target=*link02 x=980 y=550 size=20 text=第二話はこちら]',
        '@call storage="tyrano.ks"'
    ):
        print(parse_line(sample))
        print(construct_tag(parse_line(sample)))
