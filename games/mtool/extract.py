import json
from message import MessageList


with open('./data/ManualTransFile.json') as f:
    mtf = json.load(f)

message_list = MessageList()
for line in mtf:
    message_list.append(line)

message_list.flush('./data/galtransl.json')
message_list.dump_stats()
