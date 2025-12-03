#!/bin/zsh

source ./rdts/base.zsh


function tyuui() {
    out=$1
    src=$2
    text=$3
    magick $src \
        -fill black \
        -colorize 50% \
        ${title_font[@]} \
        -gravity north \
        -annotate +0+180 '注意事项' \
        -pointsize 80 \
        -strokewidth 3 \
        -annotate +0+380 "$text" \
        $out
}

tyuui $translated_dir/fgimage/tyuui_bgv.png "$original_dir/bgimage/title (1).png" $tyuii_bgv_text
tyuui $translated_dir/fgimage/tyuui_iyashi.png $original_dir/bgimage/title_6.png $tyuui_iyashi_text


function plan() {
    out=$1
    src=$2
    title=$3
    text=$4
    magick $src \
        -fill black \
        -colorize 50% \
        ${title_font[@]} \
        -gravity north \
        -interline-spacing -50 \
        -annotate +0+35 "$title" \
        -pointsize 84 \
        -strokewidth 3 \
        -gravity northwest \
        -interline-spacing 0 \
        -annotate +100+340 "$text" \
        $out
}


for i in {6..13}; do
    j=$(( ( $i - 5 )  * 3 ))
    plan \
        $translated_dir/fgimage/onasapoplan$i.png \
        "$original_dir/bgimage/${onasapoplan_texts[j-2]}" \
        "${onasapoplan_texts[j-1]}" \
        "${onasapoplan_texts[j]}"
done

magick \
    -background transparent \
    -size 1920x1080 canvas:none \
    -pointsize 72 \
    -fill white \
    -stroke black \
    -strokewidth 2 \
    -font ./data/猫啃网故障黑.otf \
    -annotate +1550+700 '距射精' \
    -pointsize 40 \
    -gravity southeast \
    -annotate +50+50 'Pages' \
    $translated_dir/fgimage/syasei_hyouji.png
