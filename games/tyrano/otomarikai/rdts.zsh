#!/bin/zsh

mkdir -p ./data/translated_img

function button() {
    local color=$1
    local text=$2
    local name=$3

    magick -size 226x91 canvas:none \
        -fill $color \
        -draw "roundrectangle 0,0 225,90 45,45" \
        -fill none -stroke white -strokewidth 2 \
        -draw "roundrectangle 5,5 220,85 45,45" \
        -gravity center \
        -fill white -stroke black -strokewidth 2 \
        -font Noto-Sans-CJK-SC-Black \
        -pointsize 60 \
        -annotate +0-5 "$text" \
        ./data/translated_img/$name

}

button '#f991b5' '是'   yes.png
button '#ade9ff' '否'   no.png
button '#ade9ff' '放弃' giveup.png


function bar() {
    local color=$1
    local name=$2

    magick ./data/app/data/image/$name \
        -fill $color \
        -draw 'rectangle 280,0 %[fx:w-281],%[fx:h]' \
        -gravity center \
        -fill white -stroke black -strokewidth 1 \
        -font Noto-Sans-CJK-SC-Black \
        -pointsize 42 \
        -annotate +0-5 '进入下一阶段' \
        data/translated_img/$name
}

bar '#bce0f5' bluebar.png
bar '#f6c4d7' pinkbar.png


source ./data/img_texts.zsh

for card text in ${(kv)CARD_TEXTS}; do
    magick data/app/data/image/$card \
        -fill white \
        -draw 'roundrectangle 12,40 %[fx:w-13],160 10,10' \
        -gravity center \
        -font Noto-Sans-CJK-SC-Bold \
        -fill '#444444' \
        -pointsize 20 \
        -annotate +0+10 $text \
        data/translated_img/$card
done
