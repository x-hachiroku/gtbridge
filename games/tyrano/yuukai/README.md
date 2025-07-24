# ロリ誘拐 連れ去り悪戯シミュレーション GalTransl-14B-V3.7翻译补丁

## 购买本体

* DLSite (限日本IP): https://www.dlsite.com/maniax/work/=/product_id/RJ01302728.html


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
