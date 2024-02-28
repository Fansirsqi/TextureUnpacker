#!/usr/bin/python
# -*- coding: UTF-8 -*-
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import plistlib
from pathlib import Path

from PIL import Image


def export_image(img: Image, pathname: str, item: dict, skey: int):
    x, y, w, h = map(int, item['frame'])

    if w == 0 or h == 0:
        w = h = 1

    key = skey

    if int(key) == 0:
        size = tuple(map(int, item['sourceSize']))
    else:
        size = (h, w) if item['rotated'] else (w, h)

    size = tuple(1 if s == 0 else s for s in size)

    ox, oy, _, _ = map(int, item['sourceColorRect'])

    if item['rotated']:
        box = (x, y, x + h, y + w)
    else:
        box = (x, y, x + w, y + h)

    image = Image.new('RGBA', size, (0, 0, 0, 0))
    sprite = img.crop(box)

    if item['rotated']:
        sprite = sprite.transpose(Image.Transpose.ROTATE_90)

    if int(key) == 0:
        image.paste(sprite, (ox, oy))
    else:
        image.paste(sprite, (0, 0))

    print(f'保存文件：{pathname}')
    image.save(pathname, 'png')


def get_frame(frame: dict) -> dict:
    base_result = {}
    if frame['frame']:
        base_result['frame'] = frame['frame'].replace('}', '').replace('{', '').split(',')
        base_result['offset'] = frame['offset'].replace('}', '').replace('{', '').split(',')
        base_result['rotated'] = frame['rotated']
        base_result['sourceColorRect'] = frame['sourceColorRect'].replace('}', '').replace('{', '').split(',')
        base_result['sourceSize'] = frame['sourceSize'].replace('}', '').replace('{', '').split(',')
    return base_result


def gen_image(file_name: str, skey: int):
    plist = Path(f'{file_name}.plist')

    if not plist.exists():
        print(f'plist文件【{plist}】不存在！请检查!!')
        return f'文件【{plist}】不存在！请检查'

    png = Path(f'{file_name}.png')
    jpg = Path(f'{file_name}.jpg')

    image_file = png if png.exists() else jpg if jpg.exists() else None

    if not image_file:
        print(f'png文件【{png}】或jpg文件【{jpg}】不存在！请检查!!')
        return f'文件【{png}】或jpg文件【{jpg}】不存在！请检查'

    export_path = file_name
    if not os.path.exists(export_path):
        try:
            os.mkdir(export_path)
        except Exception as e:
            print(e)
            return e, '文件夹创建失败'

    lp = plistlib.load(open(plist, 'rb'))
    img = Image.open(f'{image_file}')
    frames = lp['frames']
    for key in frames:
        item = get_frame(frames[key])
        export_image(img, os.path.join(export_path, key), item, skey)


def get_frames_name(file_path: str) -> str:
    plist = Path(f'{file_path}.plist')
    if not os.path.exists(plist):
        return f'[code] plist文件【{plist}】不存在！请检查'

    lp = plistlib.load(open(plist, 'rb'))
    frames = lp['frames']
    list_code = ''
    for i in frames:
        list_code += f'<frameName>{i}</frameName>\n'
    return list_code


def get_frame_xy(frame: dict) -> tuple:
    result = {'frame': frame['frame'].replace('}', '').replace('{', '').split(',')}
    x = result['frame'][0]
    y = result['frame'][1]
    return x, y


if __name__ == '__main__':
    ...