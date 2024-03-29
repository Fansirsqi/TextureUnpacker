# 针对于 `TexturePackage`打包的 `cocos2d v2(old CocoStudio)`精灵 `Plist`资源解包
>
>注*:该项目只是为了方便拆包一《火影战记》游戏中的精灵一时兴起写的，完成度基本差不多了，之余批量解包也是可以自己修改源码做到的，目前不会考虑更新了，谢谢您的理解与支持(2023-02-01)
>

## How To Build(如何构建)

### create a virtual environment(创建虚拟环境)

```bash
python -m venv venv
```

### active the virtual environment(激活虚拟环境)

- windows

```bash
.\venv\Scripts\Activate.ps1
```

- linux

```bash
.\venv\Scripts\activate
```

### install dependencies(安装依赖)

```bash
pip install -r requirements.txt
```

### build(构建)

```bash
python ./build.py
```

### windows 用户可以在[releases](https://github.com/Fansirsqi/TextureUnpacker/releases)里下载,已经构建好的二进制exe文件

## Update 2024-02-28

添加对jpg文件的支持，优化打包体积，删除多余依赖

## Update 2022-11-17

增加了`严格模式`选项，如果图片是使用`TexturePackage`等软件正常打包，使用`严格模式`即可

如果是人手写offset的文件，去除勾选`严格模式`即可

如果软件打包的资源使用`非严格模式`解压，再重新用软件打包，会造成图片偏移严重情况，请悉知

---

Added `Strict Mode` option, if the image is packed normally using software such as `TexturePackage`, use `Strict Mode`.

If the file is handwritten offset, remove the `Strict Mode` checkbox

If you use `Non-strict mode` to unpack the resources packed by software, and then repack them with software, it will cause serious image shift.

## Bugfix 2022-11-08

1. 可能解决了导出文件夹为空，但没有报错的问题
2. 修改了图标配色
3. 添加打开弹窗提示，也许这很烦人，但我尽可能的希望你看说明书
4. 忘了

---

1. May solve the problem that the export folder is empty, but no error is reported
2. modified the icon color scheme
3. Add open pop-up hint, maybe it's annoying, but I hope you read the manual as much as possible
4. Forgotten

## 2022-10-14

效果演示：<https://www.bilibili.com/video/BV1s8411s7Dv/>

1. 基于 `tkinter`的GUI界面
2. 基于[tp-png-spli](https://github.com/ShawnZhang2015/tp-png-split)
3. 在此基础上，增加了导出精灵的每一帧名字代码输出
4. 修改了传入数据结构，默认解压在和 `Plist`同名字文件夹下
5. 得益于`TkinterDnD2`实现了拖放识别文件路径

## Packaging `cocos2d v2(old CocoStudio)` sprite `Plist` resource unpacking for `TexturePackage`

1. GUI interface based on `tkinter`
2. Based on [tp-png-spli](https://github.com/ShawnZhang2015/tp-png-split)
3. On this basis, the name code output of each frame of the exported sprite is added
4. Modified the incoming data structure, the default decompression is in the folder with the same name as `Plist`
5. Thanks to `TkinterDnD2`, drag and drop to identify file paths
