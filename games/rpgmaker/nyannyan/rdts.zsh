original='./data/original_db/'
translated='./data/translated_db/'

game='[にちゃにちゃソフト] [20220826] ねむるこねこ [RJ412048] [V3.0]/www/img/characters'
mkdir -p "$translated/$game"

texts=(
     $'胸罩\nON'   $'胖次\nON'   $'连衣裙\nON'   $'嘴\n▶'   $'小穴\n▶'   $'内射\nFIN'  $'安眠药\nON'  $'眠\nON'
     $'胸罩\nOFF'  $'胖次\nOFF'  $'连衣裙\nOFF'  $'嘴\n▶▶'  $'小穴\n▶▶'  $'浇汁\nFIN'  $'安眠药\nOFF' $'眠\nOFF'
     $'胸罩\n半脱' $'胖次\n半脱' $'连衣裙\n半脱' $'嘴\nFIN' $'小穴\nOFF' $''           $''          $'擦干\n精液'

     $'胸罩\nON'   $'胖次\nON'   $'连衣裙\nON'   $'嘴\n▶'   $'小穴\n▶'   $'内射\nFIN'  $'安眠药\nON'  $'眠\nON'
     $'胸罩\nOFF'  $'胖次\nOFF'  $'连衣裙\nOFF'  $'嘴\n▶▶'  $'小穴\n▶▶'  $'浇汁\nFIN'  $'安眠药\nOFF' $'眠\nOFF'
     $'胸罩\n半脱' $'胖次\n半脱' $'连衣裙\n半脱' $'嘴\nFIN' $'小穴\nOFF' $''           $''          $'擦干\n精液'

     $'嘴\nOFF'    $''           $''             $''        $''          $''           $'称号'      $''
     $'口交\nOFF'  $''           $''             $''        $''          $''           $'称号'      $''

     $''           $''           $''             $''        $''          $''           $''          $''
     $''           $''           $''             $''        $''          $''           $'帮助'      $''
     $''           $''           $''             $''        $''          $'返回\n标题' $'存档'      $''
     $''           $''           $''             $''        $''          $''           $'自杀'      $''
)

base=30
len=180
interval=240

c1='#CFD6EB'
c2='#8395C9'
cf='#41589A'

clear_cmds=( -fill $c1 )
write_cmds=(
    -fill $cf
    -font './data/fusion-pixel-12px-monospaced-zh_hans.ttf'
    -pointsize 64
)

for i in {0..95}; do
    if (( i == 24 )) || (( i == 56 )); then
        clear_cmds+=( -fill $c2 )
    fi
    if (( i == 48 )) || (( i == 57 )); then
        clear_cmds+=( -fill $c1 )
    fi
    if [[ -z "${texts[i+1]}" ]]; then
        continue
    fi

    row=$(( i % 8 ))
    col=$(( i / 8 ))
    x=$(( base + col * interval ))
    y=$(( base + row * interval ))
    clear_cmds+=( -draw "rectangle ${x},${y},$((x + len)),$((y + len))" )
    write_cmds+=( -annotate "+$(( x + len / 2 - 1440 ))+$(( y + len / 2 - 960))" "${texts[i+1]}" )
done

magick \
    "$original/$game"/\!icon01.png \
    -gravity Center \
    -resize 500% \
    ${clear_cmds[@]} \
    ${write_cmds[@]} \
    -resize 20% \
    "$translated/$game"/\!icon01.png

node ../RPG-Maker-MV-Decrypter/cli.js e $KEY "$translated/$game"/\!icon01.png "$translated/$game"/\!icon01.rpgmvp
rm "$translated/$game"/\!icon01.png


game='[にちゃにちゃソフト] [20230310] ねむるこねこたち [RJ01036763]/www/img/pictures/'
mkdir -p "$translated/$game"

texts=(
    '插入'
    '中出'
    '口交'
    $'口内\n射精'
    $'揉捏\n胸部'

    $'舔舐\n乳头'
    $'舔舐\n小穴'
    '指奸'
    '浇汁'
    $'脱掉\n上衣'

    $'脱掉\n下装'
    $'脱掉\n胖次'
    $'显示\nUI'
    '小黑１'
    '小黑２'

    '小黑３'
    ''
    $'擦干\n精液'
    $'脱掉\n胸罩'
    '保存'

    '帮助'
    $'返回\n标题'
    $'脱掉\n胸罩'
)

for i in {001..023}; do
    if [[ -z "${texts[i]}" ]]; then
        continue
    fi
    magick \
        "$original/$game"/アイコン001.png \
        -resize 500% \
        -fill white \
        -draw 'rectangle 25,25,215,215' \
        -gravity Center \
        -fill black \
        -pointsize 64 \
        -font './data/萝莉体第二版.ttf' \
        -annotate +0+0 "${texts[i]}" \
        -resize 20% \
        "$translated/$game"/アイコン${i}.png

    node ../RPG-Maker-MV-Decrypter/cli.js e $KEY "$translated/$game"/アイコン${i}.png "$translated/$game"/アイコン${i}.rpgmvp
    rm "$translated/$game"/アイコン${i}.png
done


game='[にちゃにちゃソフト] [20250729] 通勤電車にロリっ子が乗ってはいけない理由 [RJ01437567]/img/pictures/'
mkdir -p "$translated/$game"

text='【对话指令】 与女孩子对话可获得各种效果。

　【轻度性骚扰】
　　点击时获得的涩涩点数略有增加。

　【重度性骚扰】
　　成功：点击时获得的涩涩点数大幅增加。
　　失败：危险点数增加。

　【命令】
　　成功：提升1级指令等级。（最高LV5）
　　失败：危险点数增加。
　　指令等级越高，骚扰指令增加的危险点数越小。

　【安抚】
　　降低危险点数。

　【邀请去洗手间】
　　达到一定涩涩点数后即可使用。不消耗涩涩点数。
　　成功：在洗手间和女孩子涩涩。
　　失败：增加危险点数。'

magick \
    -size 1632x1248 xc:'rgba(0,0,0,0.5)' \
    -gravity West \
    -font 'Noto-Sans-CJK-SC-Black' \
    -pointsize 38 \
    -fill black \
    -stroke white \
    -strokewidth 1 \
    -annotate +40+0 \
    "$text" \
    -resize 50% \
    "$translated/$game"/help01.png


text='【性骚扰指令】 选择身体部位并进行骚扰。
　选项越靠下风险越大，但收益也越大。
　
　选项１　　　　风险 ★　　　　收益 ★
　选项２　　　　风险 ★★　　　收益 ★★
　选项３　　　　风险 ★★★　　收益 ★★★
　
　无需消耗任何涩涩点数。
　成功：获得涩涩点数。
　失败：增加危险点数。'

magick \
    -size 1632x1248 xc:'rgba(0,0,0,0.5)' \
    -gravity West \
    -font 'Noto-Sans-CJK-SC-Black' \
    -pointsize 40 \
    -fill black \
    -stroke white \
    -strokewidth 1 \
    -annotate +40+0 \
    "$text" \
    -resize 50% \
    "$translated/$game"/help02.png


magick "$original/$game"/help03.png \
    -resize 200% \
    -font 'Noto-Sans-CJK-SC-Black' \
    -pointsize 36 \
    -fill black \
    -stroke white \
    -strokewidth 1 \
    -size 670x2000 xc:'rgba(0,0,0,0.498)' -geometry +0+0 -compose Copy -composite \
    -size 1022x220 xc:'rgba(0,0,0,0.498)' -geometry +0+0 -compose Copy -composite \
    -size 720x300 xc:'rgba(0,0,0,0.498)' -geometry +0+240 -compose Copy -composite \
    -size 1260x140 xc:'rgba(0,0,0,0.498)' -geometry +0+920 -compose Copy -composite \
    -size 920x200 xc:'rgba(0,0,0,0.498)' -geometry +0+1060 -compose Copy -composite \
    -annotate +10+60 $'【基本操作】\n　点击女孩子即可获得涩涩点数。\n　涩涩点数存在上限。' \
    -annotate +580+80 $'【乘客窗口】\n　显示在场乘客。\n　乘客在场时性骚扰女孩子\n　会增加危险值。' \
    -annotate +70+280 $'【涩涩点数】\n　进行性骚扰后上升。\n　超过一定值后即可在洗手间进行涩涩。\n【危险点数】\n　被警惕时上升。\n　超过上限后游戏结束。' \
    -annotate +240+680 $'【对话指令】\n　通过对话获得各种效果。\n【性骚扰指令】\n　性骚扰喜欢的身体部位。' \
    -annotate +940+960 $'【SKIP】\n　曾在洗手间涩涩后\n　可以直接去洗手间。' \
    -annotate +700+1120 $'\n【帮助】\n　显示此界面。' \
    -resize 50% \
    "$translated/$game"/help03.png

for f in "$translated/$game"/*.png; do
    node ../RPG-Maker-MV-Decrypter/cli.js e $KEY "$f" "${f}_"
    rm "$f"
done


game='[にちゃにちゃソフト] [20250116] すやすや電車 ～睡眠姦シミュレーション～ [RJ01324708]/img/pictures/'
mkdir -p "$translated/$game"

_base=(
    magick
    ./data/suyasuya.png
    -font 'Noto-Sans-CJK-SC-Black'
    -pointsize 30
)

_1a=(
    -fill none -stroke white -strokewidth 3
    -draw 'roundrectangle 5,5,180,70,10,10'
    -draw 'line 180,36,480,36'
    -fill white -stroke none
    -annotate +490+48 $'【剩余时间】\n　归零时游戏结束。'
)

_1b=(
    -fill none -stroke white -strokewidth 3
    -draw 'roundrectangle 0,90,400,170,10,10'
    -draw 'line 400,130,560,130'
    -fill white -stroke none
    -annotate +570+140 $'【睡眠槽】\n　到达最大时女孩子会进入朦胧状态。\n　不进行操作时自动减少。'
)

_1c=(
    -fill none -stroke white -strokewidth 3
    -draw 'roundrectangle 10,210,330,690,10,10'
    -draw 'line 330,340,450,340'
    -fill white -stroke none
    -annotate +460+350 $'【脱衣指令】\n　成功时脱掉指定的衣服。\n　失败后，女孩子会进入朦胧状态。朦胧状态时无法脱衣。'
)

_1d=(
    -fill none -stroke white -strokewidth 3
    -draw 'roundrectangle 10,700,330,1080,10,10'
    -draw 'line 330,840,490,800'
    -draw 'roundrectangle 1290,10,1610,1140,10,10'
    -draw 'line 1290,640,650,800'
    -fill white -stroke none
    -annotate +480+810 $'【触摸指令】\n　触摸时睡眠槽和技能点会增加。\n　※变更体位除外。\n　如果女孩子进入朦胧状态，请立即停止，否则游戏将结束。'
)

_1e=(
    -fill none -stroke white -strokewidth 3
    -draw 'roundrectangle 620,1010,1020,1160,10,10'
    -draw 'line 620,1085,150,1125'
    -fill white -stroke none
    -annotate +40+1135 $' 【技能】\n　消耗涩涩点数使用\n　左：增加剩余时间。　右：停止全部触摸。'
)

magick \
    -size 1632x1248 xc:'rgba(0,0,0,0)' \
    -font 'Noto-Sans-CJK-SC-Black' \
    -pointsize 30 \
    ${_1a[@]} ${_1b[@]} ${_1c[@]} ${_1d[@]} ${_1e[@]} \
    -resize 50% \
    "$translated/$game"/help01.png

${_base[@]} ${_1a[@]} -resize 50% "$translated/$game"/help01a.png
${_base[@]} ${_1b[@]} -resize 50% "$translated/$game"/help01b.png
${_base[@]} ${_1c[@]} -resize 50% "$translated/$game"/help01c.png
${_base[@]} ${_1d[@]} -resize 50% "$translated/$game"/help01d.png
${_base[@]} ${_1e[@]} -resize 50% "$translated/$game"/help01e.png
${_base[@]} ${_1a[@]} ${_1b[@]} ${_1c[@]} ${_1d[@]} ${_1e[@]} -resize 50% "$translated/$game"/help02.png

for f in "$translated/$game"/*.png; do
    node ../RPG-Maker-MV-Decrypter/cli.js e $KEY "$f" "${f}_"
    rm "$f"
done
