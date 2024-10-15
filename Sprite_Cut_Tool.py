import os
import sys
import tkinter
import tkinter.filedialog
import tkinter.messagebox

# from tkinter import *
from tkinter import IntVar, Checkbutton

from PIL import Image, ImageTk
from tkinterdnd2 import Tk, DND_FILES
import plistlib
from pathlib import Path


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

    print(f'保存文件:{pathname}')
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
        print(f'plist文件[{plist}]不存在!请检查!!')
        return f'文件[{plist}]不存在!请检查'

    png = Path(f'{file_name}.png')
    jpg = Path(f'{file_name}.jpg')

    image_file = png if png.exists() else jpg if jpg.exists() else None

    if not image_file:
        print(f'png文件[{png}]或jpg文件[{jpg}]不存在!请检查!!')
        return f'文件[{png}]或jpg文件[{jpg}]不存在!请检查'

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
        return f'[code] plist文件[{plist}]不存在!请检查'

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


def do_unpack(file_path):
    """执行解压

    :param _type_ file_path: 文件路径
    :return _type_: _description_
    """
    resault = gen_image(file_path, CheckVar1.get())
    return get_frames_name(file_path), resault


def get_resource_path(relative_path):
    """获取资源文件夹

    :param _type_ relative_path: _description_
    :return _type_: _description_
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


def drop(event):
    entry_sv.set(event.data)


def tps(sth):
    """提示框

    :param _type_ sth: _description_
    """
    tkinter.messagebox.showinfo('', sth)


def about():
    """关于"""
    entry.grid_remove()
    ex_btn.grid_remove()
    conlose.grid_remove()
    C1.grid_remove()
    auth_img.grid(row=0, column=2, columnspan=6, padx=70, pady=20)
    back_btn.grid(row=1, column=4, columnspan=2)
    tkinter.messagebox.showinfo('', 'Made_BY 依旧归七')


def back():
    """返回"""
    entry.grid()
    ex_btn.grid()
    conlose.grid()
    C1.grid()
    auth_img.grid_remove()
    back_btn.grid_remove()


def back_main_adk():
    entry.grid()
    C1.grid()
    ex_btn.grid()
    conlose.grid()
    auth_img.grid_remove()
    back_btn.grid_remove()
    askfile()


def add_menu(name, func_name):
    """添加菜单,以及菜单实现的函数名称"""
    main_menu.add_command(label=f'{name}', command=func_name)


def askfile():
    """检测输入框是否为空

    :return _type_: _description_
    """
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        entry_sv.set(filename)
    else:
        if not entry_sv.get():
            entry_sv.set('您没有选择任何Plist文件')
    return filename


def outputs(code):
    conlose.insert(tkinter.INSERT, code)


def get_path():  # sourcery skip: assign-if-exp
    if entry_sv.get() == '':
        return tps('请填入正确路径!')  # 为空,提示
    else:
        path = str(entry_sv.get()).split('.pl')[0]  # fixbug 修复GUI端路径中存在.无法识别完整文件路径问题
        print(path)
        return path


def click_btn():
    conlose.delete('1.0', 'end')  # 清空控制台
    code, resault = do_unpack(get_path())
    if CheckVar1.get() == 0:
        tips = '严格模式'
    else:
        tips = '非严格模式'
    if code is None:
        outputs(tips)
        outputs(resault)
    else:
        outputs(code)
        outputs(tips)


root = Tk()
# root.resizable(width=False, height=False)
root.iconbitmap(get_resource_path('Icon.ico'))

root.title('Sprite Cut Tool')

entry_sv = tkinter.StringVar()

if not entry_sv.get():
    entry_sv.set('您没有选择任何Plist文件')


entry = tkinter.Entry(root, textvar=entry_sv, width=59, fg='#7c7c7c', bd=2)

entry.grid(row=0, column=2, padx=10, pady=2, ipady=7, columnspan=6)


CheckVar1 = IntVar()
C1 = Checkbutton(root, text='严格模式', variable=CheckVar1, onvalue=0, offvalue=1, width=20)
C1.grid(row=1, column=2)
C1.select()


ex_btn = tkinter.Button(root, text='分解图片', relief=tkinter.RAISED, font=('楷体', 14), command=click_btn)
ex_btn.grid(row=1, column=3, columnspan=1)

conlose = tkinter.Text(root, bg='#000', fg='#00ecf7', font=('新宋体', 12), width=52, height=24)
conlose.grid(row=2, column=0, columnspan=6, padx=10, pady=2)

img_open = Image.open(get_resource_path('head.png'))
img_png = ImageTk.PhotoImage(img_open)

auth_img = tkinter.Label(root, text='绿色', image=img_png, bg='#fff', fg='#ffffff')

back_btn = tkinter.Button(root, text='返回主界面', relief=tkinter.RAISED, font=('楷体', 8), width=15, command=back)

main_menu = tkinter.Menu()
add_menu('文件', back_main_adk)
add_menu('关于', about)
root.config(menu=main_menu)

sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
rh = 440
rw = 500
rx = (sw - rw) // 2 + 25
ry = (sh - rh) // 2
root.geometry(f'{rh}x{rw}+{rx}+{ry}')

entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', drop)
tkinter.messagebox.showinfo('', '您可以拖入plist文件,\n请确保和png在同一目录,png与plist文件名相同')

root.mainloop()
