from pathlib import Path

from gtbridge import load
from gtbridge.games.mai.sct import SCT
from gtbridge.tools.uif import UIF

from extract import SCT_DICT


if __name__ == '__main__':
    json_path = Path('./data/translated_json/')
    original_blob_path = Path('./data/original_blob/')
    translated_blob_path = Path('./data/translated_blob/')
    translated_blob_path.mkdir(parents=True, exist_ok=True)

    uif = UIF()

    for s in SCT_DICT:
        sct = SCT((original_blob_path/s).read_bytes(), *SCT_DICT[s])

        for chunk in sct.chunks:
            j = (json_path / chunk.name).with_suffix('.json')
            if not j.is_file():
                print(f'Skipping {chunk.name}: translation not found.')
                continue

            translated_message_iter = iter(load(j))

            messages = chunk.get_messages()
            for i, message in enumerate(messages):
                if message and message[0] == '_':
                    continue

                translated_message = next(translated_message_iter)
                assert translated_message.original == message, (s, chunk.name)
                if len(translated_message.message) > 120:
                    print(f'Warning: message too long in {chunk.name}: "{translated_message.message}"')
                messages[i] = uif.replace(translated_message.message)

            _SENTINEL = object()
            assert next(translated_message_iter, _SENTINEL) is _SENTINEL, chunk.name

            chunk.set_messages(messages)

        (translated_blob_path/s).write_bytes(sct.to_bytes())

    uif.gen_conf('./data/uif_config.json')
