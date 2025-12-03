#!/bin/zsh

source ./rdts/base.zsh

magick $original_dir/fgimage/gamble_ikasama.png \
    -channel A \
    -region 1000x720+500+0 -evaluate set 0 \
    -gravity southwest \
    -region 625x805+0+0 -evaluate set 0 \
    -gravity southeast \
    -region 530x805+0+0 -evaluate set 0 \
    +region +channel \
    \
    -fill white \
    -stroke black -strokewidth 2 \
    -font ./data/猫啃网故障黑.otf \
    -pointsize 100 \
    -gravity north \
    -annotate +0+15 '作弊模式选择' \
    -pointsize 60 \
    -annotate -790+270 '不作弊' \
    -annotate +790+270 $'更容易\n抽中自己' \
    -annotate +50+580   $'更容易抽中\n傲娇【芽衣酱】' \
    -annotate -550+855 $'更容易抽中\n雌小鬼【柚希酱】' \
    -annotate +660+855 $'更容易抽中\n消沉系【美绪酱】' \
    $translated_dir/fgimage/gamble_ikasama.png

magick \
    -background transparent \
    -size 1920x1080 canvas:none \
    -gravity north \
    -fill white \
    -stroke black -strokewidth 2 \
    -font ./data/猫啃网故障黑.otf \
    -pointsize 100 \
    -annotate +0+50 '规则说明' \
    -pointsize 60 \
    -gravity northwest \
    -annotate +50+200 "$gamble_r1" \
    -gravity southwest \
    -annotate +50+50 "$gamble_r2" \
    $translated_dir/fgimage/gamble_rule.png

for i in {1..4}; do
    magick \
        -background transparent \
        -size 1920x1080 canvas:none \
        -gravity north \
        -pointsize 96 \
        -fill white \
        -stroke '#700707' -strokewidth 2 \
        -font ./data/zihunkuaileqiaoheiti.ttf \
        -annotate +0+35 ${gamble_rules[i]} \
        $translated_dir/fgimage/gamble_rule${i}.png
done
