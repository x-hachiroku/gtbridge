#!/bin/zsh

source ./rdts/base.zsh

magick \
    -background none \
    -size 1920x1080 canvas:none \
    -gravity north \
    -font ./data/猫啃网故障黑.otf \
    -fill white \
    -stroke black \
    -strokewidth 2 \
    -pointsize 120 \
    -annotate +0+200 '惩罚游戏时间' \
    -pointsize 80 \
    -annotate +0+400 $etd_batsu_text \
    $translated_dir/fgimage/etd_batsu.png

magick $original_dir/fgimage/etd_battleui.png \
    -region 360x60+1190+775 \
    -channel A \
    -evaluate set 0 \
    +channel +region \
    -font ./data/猫啃网故障黑.otf \
    -fill white \
    -stroke black \
    -strokewidth 2 \
    -pointsize 64 \
    -annotate +1200+840 '魔法心叶' \
    $translated_dir/fgimage/etd_battleui.png


function etd_card() {
    f=$1
    shift
    magick $original_dir/fgimage/$f \
        -alpha off \
        -fill '%[pixel:p{35,90}]' \
        -draw 'rectangle 0,0 180,45' \
        -draw 'rectangle 0,120 180,180' \
        -alpha on \
        -channel A \
        -evaluate set 90% \
        +channel \
        \( \
            $original_dir/fgimage/etd_card99.png \
            -channel A -threshold 99% \
        \) \
        -compose over -composite \
        -gravity north \
        -font ./data/猫啃网故障黑.otf \
        -fill white \
        -stroke black \
        -strokewidth 1 \
        -pointsize 28 \
        -annotate +0+15 $1 \
        -pointsize 24 \
        -annotate +0+120 $2 \
        -pointsize 22 \
        -annotate +0+145 $3 \
        $translated_dir/fgimage/$f

    cp $translated_dir/fgimage/$f $translated_dir/image/$f
}


for i in {01..22}; do
    j=$(( i * 3 ))
    etd_card \
        etd_card${i}.png \
        ${etd_cards[j-2,j]}
done


function etd_skill() {
    f=etd_$1.png
    shift
    magick $cleared_dir/image/$f \
        -gravity north \
        -font ./data/猫啃网故障黑.otf \
        -fill white \
        -stroke black \
        -strokewidth 1 \
        -pointsize 28 \
        -annotate +0+115 $1 \
        -pointsize 24 \
        -interline-spacing -10 \
        -annotate +0+145 $2 \
        $translated_dir/image/$f
}

for i in {1..12..3}; do
    etd_skill \
        ${etd_skills[i]} \
        ${etd_skills[i+1]} \
        ${etd_skills[i+2]}

done


magick -background transparent \
    -font ./data/猫啃网故障黑.otf \
    -fill white \
    -stroke black -strokewidth 2 \
    -pointsize 64 \
    -gravity center \
    'label:请选择下场战斗要使用的道具' \
    -resize x74 \
    -extent 1572x74 \
    "$translated_dir/fgimage/etd_itemsentaku.png"


magick \
    -background none \
    -size 1920x1080 canvas:none \
    -gravity north \
    -font ./data/猫啃网故障黑.otf \
    -fill white \
    -stroke black \
    -strokewidth 2 \
    -pointsize 64 \
    -annotate +0+50 '射精等待时间（一分钟后射精许可）' \
    $translated_dir/fgimage/etd_oazuke.png


magick $original_dir/fgimage/etd_sousa.png \
    -region 520x60+100+550 \
    -channel A \
    -evaluate set 0 \
    +channel +region \
    -font ./data/猫啃网故障黑.otf \
    -fill white \
    -stroke black \
    -strokewidth 1 \
    -pointsize 24 \
    -annotate +100+580 '状态UP・自慰支援难度UP' \
    -annotate +100+607 '状态DOWN・自慰支援难度DOWN' \
    $translated_dir/fgimage/etd_sousa.png
