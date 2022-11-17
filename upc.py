#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import plistlib
import sys
from PIL import Image
from pathlib import Path


def export_image(img, pathname, item, skey):  # sourcery skip: assign-if-exp

    # 去透明后的子图矩形
    x, y, w, h = tuple(map(int, item['frame']))

    # 防止宽高为0报错退出程序
    if w == 0:
        w = 1
    if h == 0:
        h = 1

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

    # rotated纹理旋转90度
    if item['rotated']:
        sprite = sprite.transpose(Image.Transpose.ROTATE_90)

    if int(key) == 0:  # 设置切图模式，0为默认模式，其他为不标准格式)
        # 粘贴子图，设置偏移 默认模式
        image.paste(sprite, (ox, oy))
    else:
        # 粘贴子图，设置偏移 非严格模式
        image.paste(sprite, (0, 0))

    # 保存到文件
    image.save(pathname, 'png')
    print(f'写入文件：{pathname} ok!')


# 获取 frame 参数
def get_frame(frame):
    result = {}
    if frame['frame']:
        result['frame'] = frame['frame'].replace(
            '}', '').replace('{', '').split(',')
        result['sourceSize'] = frame['sourceSize'].replace(
            '}', '').replace('{', '').split(',')
        result['sourceColorRect'] = frame['sourceColorRect'].replace(
            '}', '').replace('{', '').split(',')
        result['rotated'] = frame['rotated']
        # result['offset'] = frame['offset'].replace('}', '').replace('{', '').split(',')
    return result


# 生成图片
def gen_image(file_name):
    # 检查文件是否存在
    plist = Path(f'{file_name}.plist')
    if not os.path.exists(plist):
        print(f'plist文件【{plist}】不存在！请检查!!')
        return f'[导出]plist文件【{plist}】不存在！请检查'

    png = Path(f'{file_name}.png')
    if not os.path.exists(png):
        print(f'png文件【{png}】不存在！请检查!!')
        return f'[导出]png文件【{png}】不存在！请检查'

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
    print("请输入切图模式，0，标准模式，1，不严格模式")
    skey = input("请输入:")
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
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        gen_image(filename)
