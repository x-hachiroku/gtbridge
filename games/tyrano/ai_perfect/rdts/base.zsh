#!/bin/zsh

source ./data/img_texts.zsh

original_dir='./data/original/data/'
cleared_dir='./data/cleared/'
translated_dir='./data/translated/data/'
mkdir -p $translated_dir/{bgimage,fgimage,image}

title_font=(
    -pointsize 120
    -fill white
    -stroke '#00068f'
    -strokewidth 5
    -font ./data/优设标题黑.ttf
)
