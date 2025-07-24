#!/bin/zsh

mkdir -p ./data/translated_img

magick data/app/data/image/giveup.png \
    -fill '#353535'\
    -draw 'rectangle 45,30 %[fx:w-46],%[fx:h-31]' \
    -font Noto-Sans-CJK-SC-Black \
    -fill white \
    -stroke black -strokewidth 1 \
    -pointsize 60 \
    -gravity center \
    -annotate +0+0 放弃 \
    ./data/translated_img/giveup.png


BUTTON_TEXTS=(
    "aori"   "煽动的音声\n(桃狐)"
    "hiai"   "哀嚎的音声\n(日葵酱)"
    "kongan" "恳求的音声\n(日葵酱)"
)

MODE_COLORS=(
    "on"   "#ff6ce9"
    "off"  "white"
    "off2" "#353535"
)

for button text in ${(kv)BUTTON_TEXTS}; do
    for mode color in ${(kv)MODE_COLORS}; do
        magick data/app/data/image/aori_on.png \
            -fill black \
            -draw 'rectangle 50,12 %[fx:w-51],%[fx:h-13]' \
            -font Noto-Sans-CJK-SC-Black \
            -fill ${color} \
            -pointsize 26 \
            -gravity center \
            -annotate +0+0 ${text} \
            ./data/translated_img/${button}_${mode}.png
    done
done


source ./data/img_texts.zsh

for hyouji text in ${(kv)HYOUJI_TEXTS}; do
    magick data/app/data/image/hyouji_01.png \
        -fill '#111111' \
        -draw 'rectangle 10,50 %[fx:w-11],%[fx:h-51]' \
        -font Noto-Serif-CJK-SC-Black \
        -fill white \
        -pointsize 38 \
        -annotate +35+90 $text \
        data/translated_img/$hyouji
done

for mission text in ${(kv)MISSION_TEXTS}; do
    magick -background transparent \
        -font Noto-Serif-CJK-SC-Black \
        -fill white \
        -stroke black -strokewidth 2 \
        -pointsize 42 \
        -gravity center \
        "label:${text}" \
        "./data/translated_img/${mission}"
done
