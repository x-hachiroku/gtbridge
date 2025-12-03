#!/bin/zsh

source ./rdts/base.zsh

function card_active() {
    out=$1
    text=$2
    magick $original_dir/fgimage/deli_shimeityuu.png \
        -region 143x55+14+35 \
        -channel A \
        -evaluate set 0 \
        +channel +region \
        -gravity north \
        -fill '#FCFF00' \
        -stroke black \
        -strokewidth 1 \
        -pointsize 48 \
        -font ./data/萝莉体第二版.ttf \
        -annotate +0+30 $text \
        $out
}

function card_default() {
    out=$1
    text=$2
    magick \
        -background transparent \
        -size 169x266 canvas:none \
        -fill '#A1A1A1' \
        -colorize 100% \
        -channel A \
        -evaluate set 49% \
        +channel \
        -gravity center \
        -fill white \
        -pointsize 48 \
        -font ./data/萝莉体第二版.ttf \
        -annotate +0+0 $text \
        $out
}


card_active $translated_dir/fgimage/deli_aisekityuu.png '同席中'
card_active $translated_dir/fgimage/deli_sentakutyuu.png '选择中'
card_active $translated_dir/fgimage/deli_shimeityuu.png '指名中'

card_default $translated_dir/fgimage/deli_hatena.png '？？？'
card_default $translated_dir/fgimage/deli_kyuukei.png '休息中'
card_default $translated_dir/fgimage/deli_sabori.png '偷懒中'
card_default $translated_dir/fgimage/deli_sekkyakutyuu.png '接客中'
card_default $translated_dir/fgimage/deli_shimeizumi.png '已指名'
card_default $translated_dir/fgimage/deli_yobikomi.png '揽客中'

magick $cleared_dir/fgimage/deli_hukidashi.png \
    -gravity center \
    -fill '#FF2A70' \
    -pointsize 60 \
    -font ./data/萝莉体第二版.ttf \
    -annotate +0-30 '指名喜欢的女孩子吧！' \
    $translated_dir/fgimage/deli_hukidashi.png

y=110
delta_x=180
delta_y=283
delta_attr_x=40
delta_attr_y=200
attr_x=67
attr_y=18
cmds=(
    -gravity north
    -font ./data/萝莉体第二版.ttf
)
for i in {1..51..3}; do
    if (( i % 18 == 1 )); then
        y=$(( y + delta_y ))
        x=-450
        cmds+=(
            -fill white
            +stroke
            -draw "rectangle 0,$y 1920,$(( y + 25 ))"
            -strokewidth 3
        )
    fi
    c_y=$(( y + 35 ))
    cmds+=(
        -pointsize 34
        -fill black
        -stroke "rgba(%[fx:p{$(( x + 550 )),$c_y}.r*255],%[fx:p{$(( x + 550 )),$c_y}.g*255],%[fx:p{$(( x + 550 )),$c_y}.b*255],0.2)"
        -annotate +$x+$y ${deli_ichiran_texts[i]}
        +stroke
        -fill '#F68194'
        -draw 'roundrectangle '"$(( x - delta_attr_x + 545 )),$(( y - delta_attr_y )) $(( x - delta_attr_x + attr_x + 545 )),$(( y - delta_attr_y + attr_y )) 10,10"
        -fill '#FFE04F'
        -draw 'roundrectangle '"$(( x + delta_attr_x + 545 )),$(( y - delta_attr_y )) $(( x + delta_attr_x + attr_x + 545 )),$(( y - delta_attr_y + attr_y )) 10,10"
        -fill black
        -pointsize 16
        -annotate +$(( x - delta_attr_x ))+$(( y - delta_attr_y )) ${deli_ichiran_texts[i + 1]}
        -annotate +$(( x + delta_attr_x ))+$(( y - delta_attr_y )) ${deli_ichiran_texts[i + 2]}
    )
    x=$(( x + delta_x ))
done

magick $original_dir/fgimage/deli_ichiran.png \
    "${cmds[@]}" \
    $translated_dir/fgimage/deli_ichiran.png
