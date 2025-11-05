import json
from shutil import copy
from pathlib import Path
from wcwidth import wcswidth
from gtbridge import MessageList, load
from gtbridge.games.wolfrpg.wolf import handle_wolf, DATA_DIRS

original_data_dir = Path('./data/original_data/db')
original_json_dir = Path('./data/original_json/db')
translated_json_dir = Path('./data/translated_json/db')
translated_data_dir = Path('./data/translated_data/db')
original_json_dir.mkdir(parents=True, exist_ok=True)
translated_data_dir.mkdir(parents=True, exist_ok=True)

def handle_db_type_data(extract, d, message_list):
    for dd in d:
        for field in dd['data']:
            val = field.get('value')
            if not val or (not isinstance(val, str)) or val.startswith(DATA_DIRS):
                continue
            if extract:
                message_list.append(
                    val.replace('\r\n', '\n'),
                    name='ITEM',
                    original=field['value'],
                )
            else:
                message = next(message_list)
                for line in message.message.split('\n'):
                    if wcswidth(line) > 32:
                        print(f'Warning: line too long: {line}')
                text = message.message.replace('\n', '\r\n')
                field['value'] = text


def handle_db(extract, message_list):
    c_database = json.loads((original_data_dir/'CDataBase.json').read_text())
    if not extract:
        message_list = iter(load(translated_json_dir/'CDataBase.json'))
    for t in c_database['types']:
        if t['name'] == '手帳項目管理':
            handle_db_type_data(extract, t['data'], message_list)
            break
    if extract:
        message_list.flush(original_json_dir/'CDataBase.json')
    else:
        (translated_data_dir/'CDataBase.json').write_text(json.dumps(c_database, ensure_ascii=False, indent=2))

    database = json.loads((original_data_dir/'DataBase.json').read_text())
    if not extract:
        message_list = iter(load(translated_json_dir/'DataBase.json'))
    for t in database['types']:
        if t['name'] in ('もちもの管理', '読み物', '手帳内容', 'コンフィグ用カーソル位置'):
            handle_db_type_data(extract, t['data'], message_list)
    if extract:
        message_list.flush(original_json_dir/'DataBase.json')
    else:
        (translated_data_dir/'DataBase.json').write_text(json.dumps(database, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['e', 'i'])

    if parser.parse_args().mode == 'e':
        handle_wolf(extract=True)
        handle_db(extract=True, message_list=MessageList())
    else:
        handle_wolf(extract=False)
        handle_db(extract=False, message_list=None)
