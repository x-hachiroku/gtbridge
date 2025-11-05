#!/bin/zsh

mkdir -p ./data/translated_data/Picture


_title_mx=(
    '新的冒险'
    '继续探索'
    '更改设置'
    '游戏结束'
)

for i in {1..4}; do
    magick \
        -background transparent \
        -fill white \
        -stroke '#B7B9FF' -strokewidth 5 \
        -font ./data/萝莉体第二版.ttf \
        -pointsize 128 label:${_title_mx[i]} \
        \( +clone -background none -shadow 25x8-20+45 \) \
        +swap \
        -layers merge \
        -rotate -25 \
        -resize 203x \
       ./data/translated_data/Picture/title_m${i}.png
done


magick ./data/original_data/Picture/config_bg.png \
    -channel A \
    -region 180x38+80+96 -evaluate set 0 \
    -region 700x95+80+159 -evaluate set 0 \
    -region 700x38+80+280 -evaluate set 0 \
    -region 180x38+80+343 -evaluate set 0 \
    -region 180x38+80+406 -evaluate set 0 \
    -region 180x38+80+469 -evaluate set 0 \
    -region 180x38+80+532 -evaluate set 0 \
    +region +channel \
    -fill white \
    -stroke '#4f86da' -strokewidth 1 \
    -font ./data/zihunjinglingti_trial.ttf \
    -pointsize 28 \
    -annotate +306+183 $'BGM\nBGS\nSE' \
    -pointsize 30 \
    -annotate +90+120 '文本速度' \
    -annotate +90+185 '音量' \
    -annotate +90+310 '按键设定　　　 确定　　　取消　　　　　SUB' \
    -annotate +90+373 '画面效果' \
    -annotate +90+436 '脚步声' \
    -annotate +90+499 '冲刺' \
    -annotate +90+562 '手帐追加通知' \
    ./data/translated_data/Picture/config_bg.png

_menu_text='文本速度
音量

按键设定　　　确定　　　取消　　　　　　SUB
画面效果
脚步声
冲刺
手帐追加通知
'
magick \
    -background transparent \
    -size 1280x720 canvas:none \
    -fill white \
    -stroke '#4f86da' -strokewidth 1 \
    -font ./data/zihunjinglingti_trial.ttf \
    -pointsize 28 \
    -annotate +306+158 $'BGM\nBGS\nSE' \
    -pointsize 30 \
    -interline-spacing 27 \
    -annotate +100+95 $_menu_text \
    ./data/translated_data/Picture/config_bg2.png


function config() {
magick \
    -background transparent \
    -fill white \
    -stroke '#4f86da' -strokewidth 5 \
    -font ./data/zihunjinglingti_trial.ttf \
    -pointsize 128 label:$3 \
    -resize x34 \
    -gravity center \
    -extent "$2x44" \
    $1
}

config ./data/translated_data/Picture/config_1.png 376 ' 慢速　普通　快速　瞬间 '
config ./data/translated_data/Picture/config_2.png 230 ' 有　　　无 '
config ./data/translated_data/Picture/config_3.png 528 ' 始终　　　　　　　　　　　SUB键　'


for dialogue_yes in ./data/original_data/Picture/dialogue_yes?.png; do
    magick "$dialogue_yes" \
        -gravity Center \
        \( +clone \
            -blur 0x6 \
            -crop 90x50+10+0 \
        \) \
        -geometry +10+0 \
        -compose over -composite \
        -font ./data/萝莉体第二版.ttf \
        -fill white \
        -pointsize 48 \
        -annotate +0+0 '是' \
        ./data/translated_data/Picture/${dialogue_yes:t}
done


for dialogue_no in ./data/original_data/Picture/dialogue_no?.png; do
    magick "$dialogue_no" \
        -gravity Center \
        \( +clone \
            -blur 0x6 \
            -crop 150x50-10-0 \
        \) \
        -geometry -10+0 \
        -compose over -composite \
        -font ./data/萝莉体第二版.ttf \
        -fill white \
        -pointsize 48 \
        -annotate -10-5 '否' \
        ./data/translated_data/Picture/${dialogue_no:t}
done


_charas=(
    '雏'
    '夜彦'
    '樱野'
    '雪乃'
)

for c in {0..3}; do
    magick ./data/original_data/Picture/menu_chara_${c}.png \
        \( +clone \
            -blur 0x5 \
            -crop 180x43+45+472 \
        \) \
        -geometry +45+472 \
        -compose over -composite \
        -font ./data/萝莉体第二版.ttf \
        -fill white \
        -pointsize 36 \
        -annotate +110+505 ${_charas[c+1]} \
        ./data/translated_data/Picture/menu_chara_${c}.png
done


magick ./data/original_data/Picture/map.png \
    -font Noto-Sans-CJK-SC \
    -fill '#543b2f' \
    -pointsize 16 \
    -gravity North \
    -channel A \
    -region 100x30+0+45 -evaluate set 0 \
    -region 100x40+0+120 -evaluate set 0 \
    -region 30x45-90+102 -evaluate set 0 \
    -region 30x45+90+102 -evaluate set 0 \
    -region 40x30+80+10 -evaluate set 0 \
    -region 40x30+140+75 -evaluate set 0 \
    -region 60x50+0+290 -evaluate set 0 \
    -region 60x18+0+368 -evaluate set 0 \
    +region +channel \
    -annotate +0+45 '后院' \
    -annotate +0+120 $'客厅\n餐厅' \
    -annotate -90+102 $'厨\n房' \
    -annotate +90+102 $'浴\n室' \
    -annotate +80+10 '储物间' \
    -annotate +140+75 '书房' \
    -annotate +3+290 '大厅' \
    -annotate +5+365 '阳台' \
    ./data/translated_data/Picture/map.png


magick ./data/original_data/Picture/map2.png \
    -font Noto-Sans-CJK-SC \
    -fill '#543b2f' \
    -pointsize 12 \
    -gravity North \
    -channel A \
    -region 100x30+0+45 -evaluate set 0 \
    -region 100x40+0+120 -evaluate set 0 \
    -region 30x45-90+100 -evaluate set 0 \
    -region 30x45+90+100 -evaluate set 0 \
    -region 40x30+80+5 -evaluate set 0 \
    -region 40x30+140+75 -evaluate set 0 \
    -region 60x20+0+320 -evaluate set 0 \
    -region 60x18+0+387 -evaluate set 0 \
    +region +channel \
    -annotate +0+45 '后院' \
    -annotate +0+120 $'客厅\n餐厅' \
    -annotate -90+105 $'厨\n房' \
    -annotate +90+105 $'浴\n室' \
    -annotate +80+10 '储物间' \
    -annotate +140+70 '书房' \
    -annotate +0+320 '大厅' \
    -annotate +0+387 '阳台' \
    ./data/translated_data/Picture/map2.png


magick ./data/original_data/Picture/memo_hako4.png \
    -fill white \
    -draw 'rectangle 460,390 840,425' \
    -draw 'rectangle 660,390 840,440' \
    -font ./data/LongCang-Regular.ttf \
    -fill black \
    -pointsize 32 \
    -annotate 4x5+480+410 '会跳的是第几个？' \
    ./data/translated_data/Picture/memo_hako4.png


magick ./data/original_data/Picture/nekomemo.png \
    -fill '#f5f5f5' \
    -draw 'rectangle 430,190,825,300' \
    -region 440x150+410+160 \
    -blur 0x5 \
    +region \
    -font ./data/LongCang-Regular.ttf \
    -fill black \
    -pointsize 48 \
    -annotate 2x2+420+270 '把不合群的全部相乘' \
    ./data/translated_data/Picture/nekomemo.png

magick ./data/original_data/Picture/cg_gakuhu.jpg \
    \( +clone \
        -alpha extract -threshold 0 -fill black -colorize 100 \
        -stroke white -strokewidth 60 \
        -draw 'line 345,640 1250,705' \
        -stroke white -strokewidth 35 \
        -draw 'line 520,450 735,485' \
        -draw 'line 1040,500 1250,510' \
        -write mpr:mask +delete \
    \) \
    \( +clone \
        -stroke '#203471' \
        -strokewidth 25 \
        -draw 'line 345,640 1250,705' \
        -blur 0x8 \
        mpr:mask -alpha off -compose CopyOpacity -composite \
    \) \
    -compose Over -composite \
    -fill black \
    +stroke \
    -font ./data/萝莉体第二版.ttf \
    -fill '#333' \
    -pointsize 32 \
    -annotate 4x0+450+470 'd　d　h　j　　A　j　h' \
    -annotate 4x0+1000+500 'f　f　d　s　　d' \
    -font ./data/MaShanZheng-Regular.ttf \
    -fill black \
    -pointsize 51 \
    -annotate 4x0+340+655 '春　高　　楼　的　　　花　　之　　宴' \
    ./data/translated_data/Picture/cg_gakuhu.jpg
