#!/bin/zsh

source ./rdts/base.zsh

bgv_ui_buttons_c=(-830+455 -575+460 -310+460 +350+460 +590+465 +840+465)

bgv_ui_base_cmds=(
    -gravity center
    -font ./data/萝莉体第二版.ttf
    -pointsize 48
    -fill black
)

magick $cleared_dir/fgimage/bgv_ui_base.png \
    ${bgv_ui_base_cmds[@]} \
    -annotate $bgv_ui_buttons_c[1] $'返回\nBGV选择' \
    -annotate $bgv_ui_buttons_c[2] '上一个' \
    -annotate $bgv_ui_buttons_c[5] '下一个' \
    $translated_dir/fgimage/bgv_ui_base.png

function bgv_ui_button() {
    local n=$1
    shift
    magick \
        -background transparent \
        -size 1920x1080 canvas:none \
        -gravity center \
        ${bgv_ui_base_cmds[@]} \
        -annotate $@ \
        $translated_dir/fgimage/bgv_ui_$n.png
}

bgv_ui_button baon  $bgv_ui_buttons_c[3] $'播放\n序幕终幕'
bgv_ui_button baoff $bgv_ui_buttons_c[3] $'不播放\n序幕终幕'
bgv_ui_button play  $bgv_ui_buttons_c[4] '播放中'
bgv_ui_button stop  $bgv_ui_buttons_c[4] '停止中'
bgv_ui_button playlistsimple $bgv_ui_buttons_c[6] '顺序播放'
bgv_ui_button random         $bgv_ui_buttons_c[6] '随机播放'
bgv_ui_button samerepeat     $bgv_ui_buttons_c[6] '单曲循环'


sentaku_l=105
sentaku_r=1170
sentaku_t_y=145
sentaku_h_base=220
sentaku_h_delta=125

for i in {1..7}; do
    if [[ i -lt 5 ]]; then
        x=$sentaku_r
    else
        x=$sentaku_l
    fi
    sentaku_cmds=(
        -undercolor '#ddd'
        -font ./data/萝莉体第二版.ttf
        -pointsize 48
        -annotate +$x+$sentaku_t_y ${bgv_titles[i]}
        -pointsize 40
    )
    y=$sentaku_h_base
    for j in {1..5}; do
        f=bgv_${i}_${j}.png
        if [[ i -eq 1 && j -eq 5 ]]; then
            y=770
        elif [[ i -eq 5 && j -eq 3 ]]; then
            y=515
        fi
        if [[ -v bgv_texts[$f] ]]; then
            sentaku_cmds+=(
                -annotate +${x}+${y} "${bgv_texts[$f]/$'\n'/}"
            )
        fi
        y=$(( y + sentaku_h_delta ))
    done

    magick $cleared_dir/bgimage/bgv_sentaku0${i}.png \
        ${sentaku_cmds[@]} \
        +undercolor \
        ${bgv_ui_base_cmds[@]} \
        -annotate $bgv_ui_buttons_c[1] $'退出\nBGV选择' \
        -annotate $bgv_ui_buttons_c[2] $'上一页\n←' \
        -annotate $bgv_ui_buttons_c[3] $'全不选\n本页' \
        -annotate $bgv_ui_buttons_c[4] '全选本页' \
        -annotate $bgv_ui_buttons_c[5] $'下一页\n→' \
        -annotate $bgv_ui_buttons_c[6] $'开始播放\n选中的BGV' \
        $translated_dir/bgimage/bgv_sentaku0${i}.png
done


for f in "${(@k)bgv_texts}"; do
    i=${f[5]}
    j=${f[7]}
    if [[ i -eq 1 || i -eq 3 || i -eq 5 ]]; then
        x=200
    else
        x=-200
    fi
    title=${bgv_titles[i]:gs/　/}
    magick \
        -background transparent \
        -size 1920x1080 canvas:none \
        -gravity center \
        -font ./data/QingNiaoHuaGuangJianMeiHei-2.ttf \
        -pointsize 96 \
        -fill '#ea00ff' \
        -annotate +$x-300 "$title" \
        -pointsize 144 \
        -fill '#bc00cd' \
        -annotate +$x+50 "0${j}_${bgv_texts[$f]:gs/　//}.wav" \
        $translated_dir/fgimage/$f
done


magick \
    -background transparent \
    -size 1920x1080 canvas:none \
    -gravity center \
    -fill '#fffa7c' \
    -stroke black -strokewidth 2 \
    -font ./data/萝莉体第二版.ttf \
    -pointsize 80 \
    -annotate +0-300 '给把「色情语音集」当作射精许可信号使用的玩家' \
    -pointsize 72 \
    -annotate +0+100 $'由于本作品的特性，本同人作中没有「射精按钮」\n\n射精后请在色情语音选择界面选择「退出」\n 回到AI自慰支援的本篇' \
    $translated_dir/fgimage/bgvtitleafter.png


magick "$original_dir/bgimage/title (1).png" \
    -fill white \
    -colorize 50% \
    -gravity center \
    ${title_font[@]} \
    -pointsize 320 \
    -strokewidth 10 \
    -annotate +0+0 静音模式 \
    -pointsize 200 \
    $translated_dir/fgimage/nobgvmode.png
