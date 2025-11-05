#!/bin/zsh

sed -i 's/・館を探検しよう！/·在宅邸探险吧！/g' ./data/translated_data/db/CDataBase.json
sed -i 's/変更したいキーを押して下さい（Escでキャンセル）/按下想要更改的键（Esc取消）/g' ./data/translated_data/common/15_コンフィグ.json
find './data/translated_data/common' -type f -name '*.json' -exec sed -i 's/古い手帳/旧手帐/g' {} \;
find './data/translated_data/common' -type f -name '*.json' -exec sed -i 's/謎のメモ/神秘的便条/g' {} \;
find './data/translated_data/common' -type f -name '*.json' -exec sed -i 's/謎の写真と短剣/神秘的照片和短剑/g' {} \;
find './data/translated_data/common' -type f -name '*.json' -exec sed -i 's/謎の写真/神秘的照片/g' {} \;
