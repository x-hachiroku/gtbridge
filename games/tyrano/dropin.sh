#!/bin/sh

mkdir -p ./data/app/data/{scenario,image,bgimage,fgimage/default}

cp -r ./data/translated_bgimg/* ./data/app/data/bgimage/
cp -r ./data/translated_img/*   ./data/app/data/image/
cp -r ./data/translated_img/*   ./data/app/data/fgimage/
cp -r ./data/translated_img/*   ./data/app/data/fgimage/default/
cp -r ./data/translated_ks/*    ./data/app/data/scenario/
