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
button '#ade9ff' '放弃' giveup.png
button '#ade9ff' '否'   no.png


button '#f991b5' '外观' mitame.png
button '#ffde90' '气味' nioi.png
button '#ade9ff' '触感' tezawari.png


function card() {
    local alpha=$1
    local text=$2
    local name=$3

    magick ./data/app/data/image/sena1.png \
        -fill white \
        -draw 'roundrectangle 28,70 %[fx:w-28],260 10,10' \
        -gravity center \
        -font Noto-Sans-CJK-SC-Bold \
        -fill black \
        -pointsize 42 \
        -annotate +0+20 "$text" \
        -channel A -evaluate multiply $alpha \
        ./data/translated_img/$name
}

card 1 "忍耐比赛游戏\n提示:\n胖次的款式"   sena1.png
card 1 "射精诱惑游戏\n提示:\n同学八卦"     sena2.png
card 1 "疑似SEX游戏\n提示:\n小便声录音"    sena3.png
card 1 "性癖质问游戏\n提示:\n自慰声录音"   sena4.png
card 1 "胖次观察游戏\n提示:\n胖次主人特征" sena5.png
card 1 "小穴服务游戏\n提示:\n胖次主人候补" sena6.png

card 0.4 "忍耐比赛游戏\n提示:\n胖次的款式"   senab1.png
card 0.4 "射精诱惑游戏\n提示:\n同学八卦"     senab2.png
card 0.4 "疑似SEX游戏\n提示:\n小便声录音"    senab3.png
card 0.4 "性癖质问游戏\n提示:\n自慰声录音"   senab4.png
card 0.4 "胖次观察游戏\n提示:\n胖次主人特征" senab5.png
card 0.4 "小穴服务游戏\n提示:\n胖次主人候补" senab6.png


function card() {
    local alpha=$1
    local color=$2
    local text=$3
    local name=$4

    magick ./data/app/data/image/senb1.png \
        -fill white \
        -draw 'roundrectangle 28,70 %[fx:w-28],260 10,10' \
        -gravity center \
        -font Noto-Sans-CJK-SC-Black \
        -fill $color -stroke '#8f8f8f' -strokewidth 2 \
        -pointsize 96 \
        -annotate +0+10 "$text" \
        -channel A -evaluate multiply $alpha \
        ./data/translated_img/$name
}

card 1 '#ffddd2' "悠"   senb1.png
card 1 '#f5dcff' "诗音" senb2.png
card 1 '#d3e1ff' "七七" senb3.png
card 1 '#ffe4be' "光"   senb4.png
card 1 '#ffd7de' "响子" senb5.png
card 1 '#fff3c9' "仁奈" senb6.png

card 0.4 '#ffddd2' "悠"   senbb1.png
card 0.4 '#f5dcff' "诗音" senbb2.png
card 0.4 '#d3e1ff' "七七" senbb3.png
card 0.4 '#ffe4be' "光"   senbb4.png
card 0.4 '#ffd7de' "响子" senbb5.png
card 0.4 '#fff3c9' "仁奈" senbb6.png
