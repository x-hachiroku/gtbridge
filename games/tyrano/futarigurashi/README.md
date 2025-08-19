# ふたりぐらし GalTransl-14B-V3.7翻译补丁

本来以为是个以交互为主的甜品小拔，拿之前桃狐的脚本提了几千句出来感觉差不多了。替换回去发现漏了一大半。加了几个pattern变成一万来句，翻完怎么还是东漏一句西漏一句。最后直接重写了个非常暴力的脚本，好家伙提出来了两万句台词三十万字我是真没想到。
运行逻辑也复杂的离谱，自定义文本函数我找了五六个出来好像还有漏的。很多台词支离破碎，翻完感觉不如直接mtool提。
愿天堂没有embbeded expression和eval(x


## 购买本体

* DLSite: https://www.dlsite.com/maniax/work/=/product_id/RJ01214867.html


## 站内载点

安装补丁: 将`_ZH_PATCH_INSTALLER.exe`及`_ZH_PATCH_ASSETS`目录放入游戏根目录, 运行`_ZH_PATCH_INSTALLER.exe`, 等待安装完成. 安装完成后正常启动游戏即可

卸载补丁: 移除`resources/app`目录即可恢复原版

`_ZH_PATCH_INSTALLER.exe`是拿已经deprecated了几年的[pkg](www.npmjs.com/package/pkg)和[asar](www.npmjs.com/package/asar)搓出来的,
不确定兼容性怎么样, 我也不太会写js, 只在我自己的AMD64 Win10 22H2上测试过

如果遇到使用问题请在评论区反馈, 但我大概也没有什么办法. 请同时自行尝试以下手动安装方法, 或使用网盘载点的完整封包:

1. 解压`resources/app.asar`
    * 如果你有nodejs环境, 使用[electron官方asar utility](github.com/electron/asar)
      ```bash
      npm install --engine-strict @electron/asar
      npx asar extract resources/app.asar resources/app
      ```

    * 使用[asar7z 7-Zip plugin](https://www.tc4shell.com/en/7zip/asar/)
      在7-Zip安装目录下创建`Formats`目录, 将对应的dll文件放入, 然后使用7-Zip解压`resources/app.asar`至`resources/app`

    * 其他解压缩或游戏解包工具也可能支持asar格式

2. 将`_ZH_PATCH_ASSETS/app`覆盖至`resources/app`


## 网盘载点

网盘提供完整封包, 替换`resources/app.asar`即可

未完整测试, 建议备份原文件


## Credits

* [GalTransl](https://github.com/GalTransl/GalTransl)
* [SakuraLLM](https://github.com/SakuraLLM/SakuraLLM)
* [ollama](https://github.com/ollama/ollama)
