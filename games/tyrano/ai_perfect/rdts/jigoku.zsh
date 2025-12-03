#!/bin/zsh

source ./rdts/base.zsh

magick \
    -background black \
    -size 1920x1080 canvas:black \
    -alpha on \
    -channel A \
    -evaluate set 82% \
    +channel \
    -font ./data/猫啃网故障黑.otf \
    -fill white \
    -pointsize 41 \
    -annotate +70+960 "$jigoku_keiyakusyo_texts[2]" \
    -annotate +70+215 "$jigoku_keiyakusyo_texts[1]" \
    $translated_dir/fgimage/jigoku_keiyakusyo.png


magick $original_dir/fgimage/jigoku_onedot.png \
    -region 1125x80+545+220 \
    -channel A \
    -evaluate set 0 \
    +channel +region \
    -font ./data/猫啃网故障黑.otf \
    -fill white \
    -stroke black \
    -strokewidth 2 \
    -pointsize 64 \
    -gravity northeast \
    -annotate +250+200 '点击（触摸）黑色圆圈内的红点' \
    $translated_dir/fgimage/jigoku_onedot.png


function jigoku_prologue() {
    out=$1
    text=$2
    magick \
        -background black \
        -size 1920x1080 canvas:black \
        -alpha on \
        -channel A \
        -evaluate set 80% \
        +channel \
        -font ./data/猫啃网故障黑.otf \
        -fill white \
        -pointsize 72 \
        -gravity center \
        -annotate +0+0 "$text" \
        $out
}

for i in {1..3}; do
    jigoku_prologue $translated_dir/fgimage/jigoku_prologue$i.png \
        "$jigoku_prologue_texts[i]"
done


text=''
for i in {1..6}; do
    text="$text\n$jigoku_sengen_texts[i]"
    magick \
        -background transparent \
        -size 1920x1080 canvas:none \
        -font ./data/猫啃网故障黑.otf \
        -fill white \
        -stroke black \
        -strokewidth 2 \
        -pointsize 80 \
        -annotate +140+180 "$text" \
        $translated_dir/fgimage/jigoku_sengen$i.png
done


for i in {1..7}; do
    magick \
        -background transparent \
        -size 1920x1080 canvas:none \
        -font ./data/猫啃网故障黑.otf \
        -fill white \
        -stroke black \
        -strokewidth 2 \
        -pointsize 64 \
        -annotate +140+180 "$jigoku_tyoukyou_texts[i]" \
        $translated_dir/fgimage/jigoku_tyoukyou${i}.png
done

magick $translated_dir/fgimage/jigoku_tyoukyou4.png \
    \( \
        $original_dir/fgimage/jigoku_tyoukyou4.png \
        -crop 240x240+240+550 \
    \) \
    -geometry +240+550 \
    -compose over -composite \
    $translated_dir/fgimage/jigoku_tyoukyou4.png
