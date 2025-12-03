#!/bin/zsh

source ./rdts/base.zsh

function button_theme() {
    out=$1
    text=$2
    size=${3:-"318x108!"}
    magick $cleared_dir/image/button_theme.png \
        -font Noto-Sans-CJK-SC-Black \
        -pointsize 90 \
        -fill white \
        -gravity north \
        -annotate +0+40 "$text" \
        -resize $size \
        $out
}

function button_round() {
    src=$1
    out=$2
    text=$3
    pointsize=${4:-36}
    magick $src \
        -font ./data/萝莉体第二版.ttf \
        -pointsize $pointsize \
        -fill black \
        -gravity center \
        -annotate +0+0 "$text" \
        $out
}

function button_square() {
    f=$1
    text=$2
    magick $original_dir/$f \
        -fill '%[pixel:p{55,30}]' \
        -draw 'rectangle 45,20 255,106' \
        -font ./data/猫啃网故障黑.otf \
        -pointsize 54 \
        -fill white \
        -stroke black \
        -strokewidth 2 \
        -gravity center \
        -annotate +0+0 "$text" \
        $translated_dir/$f
}

button_theme $translated_dir/fgimage/endtyouki.png '中途退出' '500x170!'
button_theme $translated_dir/image/bokkikanryou.png '勃起完成'
button_theme $translated_dir/image/junbikanryou.png '准备OK'
button_theme $translated_dir/image/syasei.png '射出来了'
button_theme $translated_dir/image/giveup.png 'Give Up'
button_theme $translated_dir/image/hikinuku.png '掏出肉棒'

button_round $cleared_dir/image/button_deli.png $translated_dir/image/deli_change.png '换人' '48'
button_round $cleared_dir/image/button_deli.png $translated_dir/image/deli_kettei.png '确定' '48'
button_round $cleared_dir/image/button_deli.png $translated_dir/image/deli_nakadashi.png $'中出\n这孩子！' '40'
button_round $cleared_dir/image/button_deli.png $translated_dir/image/deli_syasei.png '射出来了' '40'

button_round $cleared_dir/image/button_c.png $translated_dir/image/hutago_junbiok.png '准备OK'

button_round $cleared_dir/image/button_y.png $translated_dir/image/hutago_syasei.png '射出来了'
button_round $cleared_dir/image/button_c.png $translated_dir/image/iyashi_kyuukeiend.png $'想重新\n开始自慰'
button_round $cleared_dir/image/button_c.png $translated_dir/image/iyashi_kyuukeistart.png '想休息一下'
button_round $cleared_dir/image/button_m.png $translated_dir/image/iyashi_syaseiganbou.png '想射出来'


magick $cleared_dir/image/button_c.png \
    -font ./data/Dymon-ShouXieTi.otf \
    -pointsize 90 \
    -fill '#0054A6' \
    -stroke white \
    -strokewidth 2 \
    -gravity center \
    -annotate +0+0 '确定' \
    $translated_dir/image/hutago_kettei.png

button_square image/etd_kettei.png '确定'
button_square image/etd_syasei.png '射出来了'
button_square image/gamble_susumu.png '前进'
button_square image/gamble_syuuryou.png '结束'
button_square image/gamble_zokkou.png '继续'
button_square image/jigoku_hayai.png '加速'
button_square image/jigoku_iikaesu.png '停止调戏'
button_square image/jigoku_kotae.png '检查答案'
button_square image/jigoku_mitomeru.png '认罪'
button_square image/jigoku_no.png '否'
button_square image/jigoku_o3.png '3次以上'
button_square image/jigoku_omorashi.png '漏出来了'
button_square image/jigoku_osoi.png '减速'
button_square image/jigoku_shinkou.png '继续调教'
button_square image/jigoku_shiohuki.png '潮吹了'
button_square image/jigoku_u3.png '3次以下'
button_square image/jigoku_yes.png '是'
button_square image/sabori.png '偷懒'
button_square image/tyoukyousaikai.png '再次调教'
