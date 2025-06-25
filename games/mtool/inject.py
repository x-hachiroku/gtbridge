import json
from message import load

translated_messages = load('./data/galtransl.json')

with open('./data/ManualTransFile.json') as f:
    mtool = json.load(f)

for m in translated_messages:
    mtool[m.original] = m.message

with open('./data/ManualTransFile.json', 'w') as f:
    json.dump(mtool, f, indent=2, ensure_ascii=False)
