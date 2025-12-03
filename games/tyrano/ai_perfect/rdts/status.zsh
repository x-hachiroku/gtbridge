#!/bin/zsh

source ./rdts/base.zsh

function get_statussheet_cmds() {
    local x=-600
    local y=207
    local delta_y=108
    cmds=(
        -pointsize 48
        -strokewidth 1
    )
    for i in {1..16}; do
        if [[ i -eq 9 ]]; then
            x=300
            y=209
        fi
        if [[ -v @[i] ]]; then
            cmds+=(
                -annotate +${x}+${y} "${@[$i]}"
            )
        fi
        y=$(( y + delta_y ))
    done
}


get_statussheet_cmds ${statussheet01_texts[@]}

magick $cleared_dir/fgimage/statussheet01.png \
    ${title_font[@]} \
    -gravity north \
    -annotate +0+35 '自慰趋势分析' \
    "${cmds[@]}" \
    -pointsize 40 \
    -annotate +300+725 '嘴' \
    -annotate +300+790 '乳头' \
    -annotate +300+855 '肛门' \
    -annotate +300+920 '会阴' \
    -annotate +300+985 '大腿内侧' \
    -annotate +845+735 '耳朵' \
    -annotate +845+840 '屁股' \
    -annotate +845+950 '睾丸' \
    $translated_dir/fgimage/statussheet01.png


get_statussheet_cmds ${statussheet02_texts[@]}

magick $cleared_dir/fgimage/statussheet02.png \
    ${title_font[@]} \
    -gravity north \
    -annotate +0+35 '性癖和性经验（问答）' \
    "${cmds[@]}" \
    $translated_dir/fgimage/statussheet02.png


get_statussheet_cmds ${statussheet03_texts[@]}

magick $cleared_dir/fgimage/statussheet03.png \
    ${title_font[@]} \
    -gravity north \
    -annotate +0+35 '自慰支援的结果' \
    "${cmds[@]}" \
    $translated_dir/fgimage/statussheet03.png

for i in {1..3}; do
    magick $translated_dir/fgimage/statussheet0${i}.png \
        -fill black \
        -colorize 50% \
        ${title_font[@]} \
        -gravity center \
        -pointsize 200 \
        -annotate +0-230 '统计数据未确定' \
        -pointsize 120 \
        -annotate +0+170 $status_mikaku_text \
        $translated_dir/fgimage/status_mikaku${i}.png
done


for i in {1..3}; do
    magick $cleared_dir/fgimage/jisseki_lock1.png \
        ${title_font[@]} \
        -gravity center \
        -pointsize 48 \
        -strokewidth 2 \
        -annotate +0+0 "达成${i}个\n成就后解锁" \
        $translated_dir/fgimage/jisseki_lock${i}.png
done


x=-535
y=-170
delta_x=360
cmds=(
)
for i in {1..8}; do
    if [[ i -eq 5 ]]; then
        x=-535
        y=215
    fi
    cmds+=(
        -pointsize 72
        -strokewidth 2
        -annotate +${x}+${y} "${jisseki_ichiran_titles[$i]}"
        -pointsize 32
        -strokewidth 0
        -annotate +$x+$(( y + 200 )) "${jisseki_ichiran_texts[$i]}"
    )
    x=$(( x + delta_x ))
done

magick $cleared_dir/bgimage/jisseki_ichiran.png \
    ${title_font[@]} \
    -gravity center \
    -annotate +0-390 '成就列表' \
    -pointsize 60 \
    -strokewidth 2 \
    -annotate +660-385 '完成' \
    ${cmds[@]} \
    $translated_dir/bgimage/jisseki_ichiran.png


magick $original_dir/fgimage/allsyoukyo.png \
    -fill Black \
    -draw 'rectangle 0,300 1920,450' \
    \
    -fill '#ffff8b' \
    -draw 'rectangle 440,610 670,690' \
    -fill '#ffa4ff' \
    -draw 'rectangle 1155,615 1590,690' \
    \
    -channel A \
    -evaluate set 82% \
    +channel \
    \
    \( +clone \
        -blur 0x3 \
        -crop 445x85+1150+610 \
    \) \
    -geometry +1150+610 \
    -compose over -composite \
    ${title_font[@]} \
    -gravity north \
    -pointsize 128 \
    -annotate +0+300 "确认要清除数据吗？" \
    -pointsize 100 \
    -strokewidth 2 \
    -annotate -400+610 "清除" \
    -annotate +400+610 "不清除" \
    $translated_dir/fgimage/allsyoukyo.png

magick \
    -background black \
    -size 1920x1080 canvas:black \
    ${title_font[@]} \
    -pointsize 200 \
    +stroke \
    -gravity center \
    -annotate +0+0 '已清除全部数据' \
    $translated_dir/fgimage/zenkeshiyes.png
