## 适用于手机端temux
先安装python环境
`pkg install python`
再安装两个依赖库，不安装则安装PIL的时候会报错

`pkg install libjpeg-turbo`
`pkg install zlib`
安装PIL
`pip install Pillow`
有可能需要安装`pip install plistlib`

使用示例
`python` upc.py "路径文件名(不要加后缀)"

```python
python upc.py "/storage/emulated/0/Download/work/ts/Shino"
```