#!/bin/zsh

source ./rdts/base.zsh


hutago_quiz_base=(
    \(
        +clone
        -crop 1x1+100+40
        +repage
        -scale '1000x65!'
    \)
    -geometry +60+6
    -compose copy -composite
    -font ./data/萝莉体第二版.ttf
    -fill white
    -stroke black
    -strokewidth 1
    -pointsize 50
    -gravity center
)
for i in {1..11}; do
    magick $original_dir/image/hutago_quiz_10a.png \
        "${hutago_quiz_base[@]}" \
        -annotate +0+0 "$hutago_quiz_texts[i]" \
        $translated_dir/image/hutago_quiz_${i}a.png

    magick $original_dir/image/hutago_quiz_10b.png \
        "${hutago_quiz_base[@]}" \
        -annotate +0+0 "$hutago_quiz_texts[i]" \
        $translated_dir/image/hutago_quiz_${i}b.png
done
