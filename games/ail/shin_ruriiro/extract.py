from pathlib import Path

from gtbridge import MessageList
from gtbridge.games.ail.sall_2006 import SALL


original_sall_dir = Path('./data/original')
original_json_dir = Path('./data/original_json')
original_json_dir.mkdir(parents=True, exist_ok=True)

message_list = MessageList()


def get_name(text):
    if text.startswith('【') and text.endswith('】'):
        return text[1:-1]
    return ''


if __name__ == '__main__':
    for sall_path in original_sall_dir.glob('*'):
        print(sall_path)
        sall = SALL(sall_path.read_bytes())
        for page in sall.pages:
            texts = page.get_texts()
            if not texts:
                continue

            if name := get_name(texts[0]):
                texts.pop(0)

            if not texts:
                continue

            name_inside = any(get_name(t) for t in texts)

            if len(texts) > 3 or name_inside:
                for text in texts:
                    if _name := get_name(text):
                        name = _name
                    else:
                        message_list.append(text, name=name)
            else:
                message_list.append('\n'.join(texts), name=name)

        if orphaned := sall.textbase.get_orphaned():
            print(f'Warning: Orphaned text in {sall_path}: {orphaned}')

        message_list.flush(original_json_dir / sall_path.with_suffix('.json').name)

    message_list.dump_stats('./names.json')
