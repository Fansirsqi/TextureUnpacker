#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import plistlib
from pathlib import Path

from PIL import Image


def export_image(img, pathname, item, skey):  # sourcery skip: assign-if-exp
    print(pathname)
    # 去透明后的子图矩形
    x, y, w, h = tuple(map(int, item['frame']))

    # 防止宽高为0报错退出程序
    if w == 0 or h == 0:
        w = h = 1

    key = skey  # 设置切图模式

    # 子图原始大小
    if int(key) == 0:  # 设置切图模式，0为默认模式，其他为不标准格式)
        size = tuple(map(int, item['sourceSize']))
        print(size)
    else:
        if item['rotated']:
            size = tuple([h, w])
            print(size)
        else:
            size = tuple([w, h])
            print(size)

    # 防止PIL报错
    for i in range(len(size)):
        if size[i] == 0:
            size = list(size)
            # print(type(size))
            size[i] = 1
            size = tuple(size)

    # 子图在原始图片中的偏移
    ox, oy, _, _ = tuple(map(int, item['sourceColorRect']))
    # 获取子图左上角，右下角
    if item['rotated']:
        box = (x, y, x + h, y + w)
    else:
        box = (x, y, x + w, y + h)

    # 使用原始大小创建图像，全透明
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    # 从图集中裁剪出子图
    sprite = img.crop(box)

    # rotated纹理旋转90度(这样旋转之后的图片就会重新旋转然后输出)
    if item['rotated']:
        sprite = sprite.transpose(Image.Transpose.ROTATE_90)

    if int(key) == 0:  # 设置切图模式，0为默认模式，其他为不标准格式)
        # 粘贴子图，设置偏移 默认模式
        image.paste(sprite, (ox, oy))
    else:
        # 粘贴子图，设置偏移 非严格模式
        image.paste(sprite, (0, 0))

    # 保存到文件
    print(f'保存文件：{pathname}')
    image.save(pathname, 'png')


# 获取 frame 参数
def get_frame(frame):
    base_result = {}
    if frame['frame']:
        base_result['frame'] = frame['frame'].replace('}', '').replace('{', '').split(',')
        base_result['offset'] = frame['offset'].replace('}', '').replace('{', '').split(',')
        base_result['rotated'] = frame['rotated']
        base_result['sourceColorRect'] = frame['sourceColorRect'].replace('}', '').replace('{', '').split(',')
        base_result['sourceSize'] = frame['sourceSize'].replace('}', '').replace('{', '').split(',')
    return base_result


# 生成图片
# skey 切图模式
def gen_image(file_name, skey):
    # 检查文件是否存在
    plist = Path(f'{file_name}.plist')
    if not os.path.exists(plist):
        print(f'plist文件【{plist}】不存在！请检查!!')
        return f'[导出]plist文件【{plist}】不存在！请检查'

    png = Path(f'{file_name}.png')
    if not os.path.exists(png):
        print(f'png文件【{plist}】不存在！请检查!!')
        return f'[导出]png文件【{plist}】不存在！请检查'

    # 检查导出目录
    export_path = file_name  # 设置为原来的目录fixupdate

    if not os.path.exists(export_path):
        try:
            os.mkdir(export_path)
        except Exception as e:
            print(e)
            return e, "文件夹创建失败"

    # 使用plistlib库加载 plist 文件

    lp = plistlib.load(open(plist, 'rb'))
    # 加载 png 图片文件
    img = Image.open(f'{file_name}.png')

    # 读取所有小图数据
    frames = lp['frames']
    for key in frames:
        item = get_frame(frames[key])
        export_image(img, os.path.join(export_path, key), item, skey)


def get_frames_name(file_path):
    plist = Path(f'{file_path}.plist')
    if not os.path.exists(plist):
        return f'[code] plist文件【{plist}】不存在！请检查'
    # im = Path(r'C:\Users\admin\Documents\WeChat Files\wxid_6ri1myvcfaw222\FileStorage\File\2022-10\work\Choji.png')
    lp = plistlib.load(open(plist, 'rb'))
    # img = Image.open(f'{im}')
    frames = lp['frames']
    # # print(frames)
    list_code = ''
    for i in frames:
        list_code = f'{list_code}<frameName>{i}</frameName>\n'
    return list_code


def get_frame_xy(frame):
    result = {'frame': frame['frame'].replace(
        '}', '').replace('{', '').split(',')}
    # print(type(result['frame']))
    x = result['frame'][0]
    y = result['frame'][1]
    return x, y


# Press the green button in the gutter to run the script.
# sourcery skip: merge-nested-ifs
if __name__ == '__main__':
    # get_frames_name(r'C:\Users\admin\Desktop\naruto\assets\Tiles\tile')
    # print("获取当前文件路径——" + os.path.realpath(__file__))
    # pwd = os.getcwd()
    # print("当前运行文件路径" + pwd)
    pass
    # load plist
    plist_conf = Path(r'C:\Users\admin\Desktop\naruto\assets\Element\HokageMinato\HokageMinato.plist')
    if not os.path.exists(plist_conf):
        print("plist文件不存在！")
    else:
        print("读取plist..")
    pl = plistlib.load(open(plist_conf, 'rb'))
    frames = pl['frames']
    # print(frames)
    result = {}
    for key in frames:
        item = get_frame(frames[key])
        result[key] = item
        with open(file='load_plist.json', mode='a', encoding='utf-8') as file:
            file.write(f"'{key}':{str(result[key])},\n")

    # gen_image(r'C:\Users\admin\Documents\WeChat Files\wxid_6ri1myvcfaw222\FileStorage\File\2022-10\work\Choji')
    # if len(sys.argv) == 3:
    #     filename = sys.argv[1]
    #     exportPath = sys.argv[2]
    #     gen_image(filename, exportPath)
