#!/bin/zsh

source ./rdts/base.zsh

magick $cleared_dir/bgimage/title.png \
    ${title_font[@]} \
    -gravity north \
    -pointsize 60 \
    -strokewidth 2 \
    -annotate -680+690 '统计数据' \
    -annotate -680+830 '成就' \
    -annotate -680+970 '变更主插画' \
    -annotate +710+95 'BGM设定' \
    -annotate +710+235 'BGV设定' \
    -annotate +710+375 '设置' \
    $translated_dir/bgimage/title.png


magick $cleared_dir/bgimage/main_eshi_sentaku.png \
    ${title_font[@]} \
    -gravity north \
    -annotate -300+70 '主插画选择' \
    -pointsize 60 \
    -strokewidth 2 \
    -annotate +620+115 $'确定' \
    $translated_dir/bgimage/main_eshi_sentaku.png


magick $cleared_dir/fgimage/firstsentakushi.png \
    ${title_font[@]} \
    -pointsize 280 \
    -strokewidth 12 \
    \( \
        $original_dir/bgimage/title.png \
        -fill black \
        -colorize 50% \
        -fill white \
        -gravity center \
        -annotate +0+0 $'接受\nAI自慰支援' \
        -resize 620x \
    \) \
    -gravity northwest \
    -geometry +225+140 \
    -compose over -composite \
    \( \
        $original_dir/bgimage/doujin_sentaku7.png \
        -crop 1700x960+105+60 \
        -resize 1920x \
        -fill black \
        -colorize 50% \
        -fill white \
        -gravity center \
        -annotate +0+0 $'使用\n同人in同人作品' \
        -resize 620x \
    \) \
    -gravity northwest \
    -geometry +1080+140 \
    -compose over -composite \
    -gravity center \
    -pointsize 92 \
    -strokewidth 3 \
    -annotate -530+260 $'考虑是否自慰' \
    -annotate +530+260 $'自慰报告\n（射精后）' \
    -pointsize 60 \
    -strokewidth 2 \
    -annotate +0+140 '确认自慰支援\n的规则' \
    -annotate +0+375 '清除所有数据'\
    $translated_dir/fgimage/firstsentakushi.png


magick $cleared_dir/fgimage/tyouki_sentaku.png \
    ${title_font[@]} \
    -gravity north \
    -annotate -40+35 '长期射精管理菜单' \
    -pointsize 60 \
    -strokewidth 2 \
    -annotate +0+215 '日数（次数）选择' \
    -annotate -40+570 '类型选择' \
    -annotate -390+720 '数日射精管理' \
    -annotate +330+720 '一日射精管理' \
    -pointsize 48 \
    -annotate -390+840 $'在选择的天数内每天1次\n10-30分钟左右的自慰支援\n在最终日获得射精许可' \
    -annotate +330+840 $'在10分钟至三小时的时间内\n接受选定次数的自慰支援\n在最后一次获得射精许可' \
    -gravity northwest \
    -annotate +1730+930 '确定' \
    $translated_dir/fgimage/tyouki_sentaku.png

cp $translated_dir/fgimage/tyouki_sentaku.png $translated_dir/bgimage/tyouki_sentaku.png


magick $original_dir/fgimage/shitumon_8_seiheki.png \
    -gravity southwest \
    -region 640x360+0+0 \
    -channel A \
    -evaluate set 0 \
    +channel +region \
    ${title_font[@]} \
    -gravity center \
    -annotate -620+340 $'选择\n自慰支援' \
    $translated_dir/fgimage/shitumon_8_seiheki.png


x=460
y=190
delta_y=215
cmds=(
    -pointsize 40
    -strokewidth 1
)
for i in {1..8}; do
    if [[ i -eq 5 ]]; then
        x=1315
        y=190
    fi
    cmds+=(
        -annotate +${x}+${y} "${doujintokuchou_texts[$i]}"
    )
    y=$(( y + delta_y ))
done

magick $cleared_dir/fgimage/doujintokuchou.png \
    ${title_font[@]} \
    -gravity north \
    -annotate +0+35 '同人in同人作品的特点' \
    -gravity northwest \
    \( \
        $original_dir/bgimage/title.png \
        -pointsize 200 \
        -gravity center \
        -annotate +0+0 $'和爱酱涩涩\n（AI自慰支援限定）' \
        -resize 350x \
    \) \
    -gravity northwest \
    -geometry +955+825 \
    -compose over -composite \
    "${cmds[@]}" \
    $translated_dir/fgimage/doujintokuchou.png


magick "$original_dir/fgimage/jaket (8).png" \
    ${title_font[@]} \
    -pointsize 200 \
    -strokewidth 6 \
    -gravity center \
    -annotate +0+0 $'不使用同人in同人作品\n（对爱酱射精吧）' \
    "$translated_dir/fgimage/jaket (9).png"

magick $original_dir/fgimage/doujin_sentaku8.png \
    \( \
        "$translated_dir/fgimage/jaket (9).png" \
        -resize 730x \
    \) \
    -geometry +590+280 \
    -compose copy -composite \
    $translated_dir/fgimage/doujin_sentaku8.png



for i in {1..5}; do
    magick \
        -size 1920x1080 canvas:white \
        -alpha on \
        -channel A \
        -evaluate set 60% \
        +channel \
        ${title_font[@]} \
        -pointsize 180 \
        -gravity center \
        -annotate +0+0 "${rules[$i]}" \
        $translated_dir/fgimage/rule$i.png
done


x=200
y=230
delta_y=285
delta_t_x=380
delta_t_y=-20
cmds=()
for i in {1..3}; do
    cmds+=(
        -pointsize 68
        -annotate +${x}+${y} ${onasapo_sentaku_titles[i]}
        -pointsize 56
        -annotate +$(( x + delta_t_x ))+$(( y + delta_t_y )) ${onasapo_sentaku_texts[i]}
    )
    y=$(( y + delta_y ))
done

magick $cleared_dir/fgimage/onasapotype_sentaku.png \
    ${title_font[@]} \
    -gravity north \
    -annotate +0+35 '自慰支援类型选择' \
    -gravity northwest \
    -pointsize 60 \
    -strokewidth 2 \
    -annotate +1715+100 '确定' \
    ${cmds[@]} \
    -pointsize 42 \
    -annotate +580+415 '（※在同人in同人作品中选择地狱级自慰支援时除外。）' \
    $translated_dir/fgimage/onasapotype_sentaku.png

cp $translated_dir/fgimage/onasapotype_sentaku.png $translated_dir/bgimage/onasapotype_sentaku.png


magick $cleared_dir/fgimage/onasapolevel_sentaku.png \
    ${title_font[@]} \
    -gravity north \
    -annotate +0+35 '自慰支援等级选择' \
    -pointsize 60 \
    -strokewidth 2 \
    -annotate -420+215 '难易度选择' \
    -annotate +420+215 '惩罚游戏有无' \
    -annotate -420+570 '时间选择' \
    -annotate +420+570 '同人in同人作品切换时间' \
    -annotate +0+925 '确定' \
    $translated_dir/fgimage/onasapolevel_sentaku.png

cp $translated_dir/fgimage/onasapolevel_sentaku.png $translated_dir/bgimage/onasapolevel_sentaku.png


magick $cleared_dir/fgimage/onasapolevel_kakunin.png \
    ${title_font[@]} \
    -gravity north \
    -annotate +0+35 '确认自慰支援等级' \
    -pointsize 60 \
    -strokewidth 2 \
    -annotate -420+215 '难易度选择' \
    -annotate +420+215 '同人in同人作品' \
    -annotate -420+570 '时间选择' \
    -annotate +0+925 '确定' \
    $translated_dir/fgimage/onasapolevel_kakunin.png


magick $cleared_dir/fgimage/slideshow_sentaku.png \
    ${title_font[@]} \
    -gravity north \
    -annotate -300+70 '配菜插画选择' \
    -pointsize 48 \
    -strokewidth 2 \
    -annotate +620+95 $'不使用\n幻灯片功能' \
    -write $translated_dir/fgimage/slideshow_sentaku.png \
    $original_dir/bgimage/nologotitle.png \
    +swap \
    -gravity center\
    -composite \
    $translated_dir/fgimage/okazu_eshi_sentaku.png

cp $translated_dir/fgimage/okazu_eshi_sentaku.png $translated_dir/bgimage/okazu_eshi_sentaku.png


x=130
y=230
delta_y=270
cmds=(
    -gravity northwest
    -pointsize 64
    -strokewidth 2
)
for i in {1..5}; do
    if [[ i -eq 4 ]]; then
        x=1040
        y=230
    fi
    cmds+=(
        -annotate +${x}+${y} ${onasapohoushin_sentaku_titles[i]}
    )
    y=$(( y + delta_y ))
done

x=530
y=190
cmds+=( -pointsize 48 )
for i in {1..5}; do
    if [[ i -eq 4 ]]; then
        x=1440
        y=190
    fi
    cmds+=(
        -annotate +${x}+${y} ${onasapohoushin_sentaku_texts[i]}
    )
    y=$(( y + delta_y ))
done

magick $cleared_dir/fgimage/onasapohoushin_sentaku.png \
    ${title_font[@]} \
    -gravity north \
    -annotate +0+35 '今天的自慰支援方针' \
    "${cmds[@]}" \
    -pointsize 60 \
    -strokewidth 2 \
    -annotate +1690+930 '确定' \
    $translated_dir/fgimage/onasapohoushin_sentaku.png

cp $translated_dir/fgimage/onasapohoushin_sentaku.png $translated_dir/bgimage/onasapohoushin_sentaku.png


magick $cleared_dir/fgimage/percentage_map.png \
    ${title_font[@]} \
    -gravity north \
    -annotate +0+35 '勃起度检查' \
    -pointsize 60 \
    -strokewidth 2 \
    -annotate +0+215 '勃起百分比' \
    $translated_dir/fgimage/percentage_map.png


y1=325
y2=635
karenda=(
    -pointsize 48
    -strokewidth 1
    -annotate +0+$(( y1 - 50 )) '上周'
    -annotate -575+$y1 '14天前'
    -annotate +0+$(( y2 - 50 )) '本周'
    -annotate -575+$y2 '7天前'
)

for d in {13..8}; do
    delta=$((13 - d + 1))
    _x=$(( -575 + delta * 192 ))
    _d=$(( d - 7 ))
    if [[ _d -eq 1 ]]; then
        _d='昨天'
    fi
    karenda+=(
        -annotate +${_x}+$y1 "$d"
        -annotate +${_x}+$y2 "$_d"
    )
done

magick $cleared_dir/bgimage/H_karenda2.png \
    ${title_font[@]} \
    -gravity north \
    -annotate +0+110 '自慰日历' \
    ${karenda[@]} \
    $translated_dir/bgimage/H_karenda2.png

magick $cleared_dir/fgimage/H_karenda.png \
    ${title_font[@]} \
    -gravity north \
    -annotate +0+110 '射精日历' \
    ${karenda[@]} \
    $translated_dir/fgimage/H_karenda.png

magick $cleared_dir/fgimage/H_karenda2.png \
    ${title_font[@]} \
    -gravity north \
    -annotate +0+110 '射精日历' \
    ${karenda[@]} \
    -gravity northwest \
    -annotate +1550+930 '完成' \
    $translated_dir/fgimage/H_karenda2.png


magick $original_dir/fgimage/H_syaseikancheck.png \
    -fill '#8190ff' \
    -draw 'rectangle 1485,780 1710,860' \
    \( +clone \
        -blur 0x5 \
        -crop 245x100+1470+770 \
    \) \
    -geometry +1470+770 \
    -compose over -composite \
    ${title_font[@]} \
    -gravity north \
    -region 900x92+0+140 \
    -channel A \
    -evaluate set 0 \
    +channel +region \
    -annotate +0+140 '射精感检查' \
    -gravity northwest \
    -pointsize 84 \
    -strokewidth 2 \
    -annotate +1525+795 '确定' \
    $translated_dir/fgimage/H_syaseikancheck.png


magick $original_dir/bgimage/title.png \
    -fill black \
    -colorize 50% \
    ${title_font[@]} \
    -gravity center \
    -pointsize 200 \
    -annotate +0+0 '自慰支援内容规划中' \
    $translated_dir/fgimage/planning_now.png


magick $original_dir/bgimage/title.png \
    -fill black \
    -colorize 50% \
    ${title_font[@]} \
    -gravity center \
    -pointsize 160 \
    -annotate +0-80 'Congratulations!!' \
    -pointsize 120 \
    -annotate +0+100 '让我们继续开发的性感带加深性癖吧' \
    -gravity southwest \
    -pointsize 64 \
    -strokewidth 2 \
    -annotate +50+50 $'您可以关闭APP了\n感谢游玩到最后' \
    $translated_dir/fgimage/congratulations.png


magick $original_dir/bgimage/title.png \
    -fill black \
    -colorize 50% \
    ${title_font[@]} \
    -pointsize 64 \
    -strokewidth 2 \
    -gravity southwest \
    -annotate +50+50 $'您可以关闭APP了\n感谢游玩到最后' \
    $translated_dir/fgimage/result.png
